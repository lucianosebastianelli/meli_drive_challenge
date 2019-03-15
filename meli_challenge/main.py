#!/usr/bin/env python3

from __future__ import print_function

import base64
import auth
import argparse
import customMySql
import httplib2
from time import gmtime, strftime
from email.mime.text import MIMEText

import mysql.connector
from apiclient import errors
from googleapiclient.discovery import build

__author__ = "Luciano Sebastianelli"
__copyright__ = "Copyright 2019, MELI Drive Challenge Project"
__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Luciano Sebastianelli"
__email__ = "lucianosebastianelli@gmail.com"
__status__ = "Prototype"

#The db_properties dictionary is used to store the Database conection properties
db_properties = {
    'host': str,
    'user': str,
    'password': str,
    'database': str,
    'f_table': str,
    'p_h_table': str
    }

#The mime_type_dic dictionary is used to determine the file extention -> Modify as needed
mime_type_dic = {
    'text/html': 'html',
	'application/zip' : 'zip',
    'text/plain' : 'txt',
    'application/rtf' : 'rtf',
    'application/vnd.oasis.opendocument.text' : 'Open Office doc',
    'application/pdf' : 'pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document' : 'MS Word document',
    'application/epub+zip' : 'EPUB',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' : 'MS Excel',
    'application/x-vnd.oasis.opendocument.spreadsheet' : 'Open Office sheet',
    'text/csv' : 'csv',
    'text/tab-separated-values' : 'tsv',
    'image/jpeg' : 'jpeg',
    'image/png' : 'png',
    'image/svg+xml' : 'svg',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation' : 'MS PowerPoint',
    'application/vnd.oasis.opendocument.presentation' : 'Open Office presentation',
    'application/vnd.google-apps.script+json' : 'json',
    'application/vnd.google-apps.audio': '',
    'application/vnd.google-apps.document':'Google Docs',
    'application/vnd.google-apps.drawing' : 'Google Drawing',
    'application/vnd.google-apps.file' : 'Google Drive file',
 	'application/vnd.google-apps.folder' : 'Google Drive folder',
    'application/vnd.google-apps.form' : 'Google Forms',
    'application/vnd.google-apps.fusiontable' : 'Google Fusion Tables',
    'application/vnd.google-apps.map' : 'Google My Maps',
    'application/vnd.google-apps.photo' : '',
    'application/vnd.google-apps.presentation' : 'Google Slides',
    'application/vnd.google-apps.script' : 'Google Apps Scripts',
    'application/vnd.google-apps.site' : 'Google Sites',
    'application/vnd.google-apps.spreadsheet' : 'Google Sheets',
    'application/vnd.google-apps.unknown' : '',
    'application/vnd.google-apps.video': '',
    'application/vnd.google-apps.drive-sdk': '',
    'application/octet-stream': '',
}

# If modifying these scopes, delete the file token.pickle.
"""
Author notes about the SCOPES:
    According to Google's documentation in order to delete a permission, the SCOPE to 
    use can be ether /auth/drive or /drive.file . In the practice, if we want to use the 
    /drive.file SCOPE, we'll get a 403 error: "The user has not granted the app write 
    access to the file.". Therefore, /auth/drive SCOPE will be used.
"""
SCOPES = [#'https://www.googleapis.com/auth/drive.readonly', #Getting files atributes
          #'https://www.googleapis.com/auth/drive.file',
          #'https://www.googleapis.com/auth/drive.metadata', #Getting and Changing permissions
          'https://www.googleapis.com/auth/drive', #Full permissions in order to get the API working
          'https://www.googleapis.com/auth/gmail.compose']#Sending emails

CLIENT_CREDENTIALS_FILE = './credentials.json' #credencials to use the project
TOKEN_PICKLE_FILE = './token.pickle' #user credencials
config_file = './config'    #Used to register the last run
myEmail = '' #GP variable used for avoiding apis requests
first_run = False

authInstance = auth.auth(SCOPES,CLIENT_CREDENTIALS_FILE, TOKEN_PICKLE_FILE)
credencials = authInstance.getCredentials()
http = httplib2.Http()

drive_service = build('drive', 'v3', credentials=credencials) #Service instance to access G-Drive-API
mail_service = build('gmail', 'v1', http=http) #Service instance to access G-Mail-API

current_run_time = strftime("%Y-%m-%dT%H:%M:%S.000Z", gmtime())




def getLastRunTime(FILE_PATH):
    with open(FILE_PATH, 'a+') as fd:
        fd.seek(0)
        LAST_RUN_T = fd.read(19)
    if not LAST_RUN_T:
        LAST_RUN_T = '1979-01-01T00:00:00'
        return LAST_RUN_T
    return LAST_RUN_T

def saveCurrentRunTime(FILE_PATH, THIS_RUN_T):
    with open(FILE_PATH, 'w+') as fd:
        fd.write(THIS_RUN_T)
    return

def removePermission(DRIVE_SERVICE, FILE_ID, PERMISSION_ID):
    """Remove a permission on a given file id.

        Args:
          DRIVE_SERVICE: Drive API service instance.
          FILE_ID: ID of the file to remove the permission. It is Google Drive API formated.
          PERMISSION_ID: ID of the permission to remove.
    """
    try:
        DRIVE_SERVICE.permissions().delete(fileId=FILE_ID, permissionId=PERMISSION_ID).execute()
    except errors.HttpError as err:
        print('An error occurred: '+str(err))
        return False
    return True


def getFileOwner(FILE):
    """Get the owner of a given file.

    :param FILE: File formated as Google Drive API
    :return: The owner email
    """
    isItMine = FILE['ownedByMe']

    for o in FILE['owners']:
        # Logical XOR comparison: if isItMine == TRUE -> returns myEmail | if not, the first owner being found
        if not isItMine != o['me']:
            return o['emailAddress']

    print("The file %s has no owner!! Contact Google for help!!!" %(FILE['name']))
    return ''

def send_message(MAIL_SERVICE, USER_ID, MESSAGE):
  """Send an email message.

  Args:
    MAIL_SERVICE: Authorized Gmail API service instance.
    USER_ID: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    MESSAGE: Message to be sent.

  Returns:
    Sent Message.

  Author Notes:
  THIS MODULE DOES NOT WORK PROPERLY!!
  GOOGLE MAIL API SEEMS TO BE BROKEN WITH PYTHON VERSION 3 OR SUPERIOR
  """
  try:

    message = (MAIL_SERVICE.users().messages().send(userId=USER_ID, body=MESSAGE).execute())
    print('Message Id: %s' %message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: '+ str(error))
    print('Se produjo un error al intentar enviar un mail. En caso de recibir el'
          ' error 401 "Login Required", probar el contenido de RAW en la app de google:\n\n'
          'https://developers.google.com/gmail/api/v1/reference/users/messages/send\n\n'
          'RAW = %s\n' %MESSAGE['raw'])

def create_message(SENDER, TO, SUBJECT, MESSAGE_P_TEXT):
  """Create a message for an email.

  Args:
    SENDER: Email address of the sender. This field won't be required
            since the logged user will be sending the email.
    TO: Email address of the receiver.
    SUBJECT: The subject of the email message.
    MESSAGE_P_TEXT: The text of the email message.

  Returns:
    An object containing a base64url encoded email object. [CHANGED]

  Author's modification:
    NOW RETURS A BASE64URL DECODED, OTHERWISE IT BROKES
  """
  message = MIMEText(MESSAGE_P_TEXT, 'html')
  toField =''
  for t in TO:
      toField += " " + str(t) + ";"
  message['from'] = ''   #DO NOT NEEDED
  message['to'] = toField
  message['subject'] = SUBJECT
  raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

  return {"raw": raw}

def notifyPubChangeByEmail(MAIL_SERVICE, FILE):
    """Notify the FILE owners that the visibility status will change from Public to Private.

    :param MAIL_SERVICE: mail service instance.
    :param FILE: a given file on Google Drive's API format

    """
    receips = list()
    for owner in FILE['owners']:
        receips.append(owner['emailAddress'])

    base64EncodedMessage = create_message('me', receips, 'Modificacion de Visibilidad',
                                          'Señor usuario, se le notifica que el archivo o carpeta'
                                          ' %s ha sido modificado y su visibilidad ha pasado de '
                                          'ser PUBLICA a PRIVADA.' %FILE['name'])

    send_message(MAIL_SERVICE, 'me', base64EncodedMessage)

def isPub(FILE):
    """Evaluate if the FILE is Public or Private

    :param FILE: a given file Google Drive API formated
    :return: True or False
    """

    if not FILE['shared']:
        return False
    for p in FILE['permissions']:
        if p['id'] == 'anyone':
            return True
    return False

def insertNewFilesAndReturnPubs(FILE_LIST, DB_CON):
    """Given a LIST OF FILES, add them to the given Database.

    :param FILE_LIST: list of files on Google Drive's API format.
    :param DB_CON: connection instance on database.
    :return: list of files that are public on Google Drive's API format.
    """
    pubs_files = list()

    try:
        DB_CON.autocommit = False
        db_cur = DB_CON.cursor()

        for f in FILE_LIST:

            isFilePub = isPub(f)
            owner = getFileOwner(f)
            insert_query = "INSERT INTO %s (id, name, extention, owner, public, modifiedTime, trashed) " \
                           "VALUES ('%s', '%s', '%s', '%s', %s, '%s', %s);" % (db_properties['f_table'],
                                                                               f['id'],
                                                                               f['name'],
                                                                               mime_type_dic[f['mimeType']],
                                                                               owner,
                                                                               isFilePub,
                                                                               f['modifiedTime'],
                                                                               f['trashed'])
            # print('atempt: ' + insert_query)
            db_cur.execute(insert_query)
            if isFilePub:
                pubs_files.append(f)

        DB_CON.commit()
        # print('Los archivos nuevos fueron registrados en %s' % (db_properties['f_table'],))

    except mysql.connector.Error as err:
        print("Error al intentar insertar en la tabla. Código de error: %d. ROLLBACK" %(err))

        DB_CON.rollback()
        pubs_files.clear()

    else:
        db_cur.close()

    finally:
        return pubs_files

def updateOldFilesAndReturnPubs(FILE_LIST, DB_CON):
    """Given a LIST OF OLD FILES, update them to the given Database.

    :param FILE_LIST: list of files on Google Drive's API format.
    :param DB_CON: connection instance on database.
    :return: list of files that are public on Google Drive's API format.
    """
    pubs_files = list()

    try:
        DB_CON.autocommit = False
        db_cur = DB_CON.cursor()

        for f in FILE_LIST:

            isFilePub = isPub(f)
            owner = getFileOwner(f)
            update_query = "UPDATE %s SET name = '%s', extention = '%s', owner = '%s', public = %s," \
                           " modifiedTime = '%s', trashed = %s WHERE id LIKE '%s'" % (db_properties['f_table'],
                                                                                      f['name'],
                                                                                      mime_type_dic[f['mimeType']],
                                                                                      owner,
                                                                                      isFilePub,
                                                                                      f['modifiedTime'],
                                                                                      f['trashed'],
                                                                                      f['id'])
            # print('atempt: ' + update_query)
            db_cur.execute(update_query)
            if isFilePub:
                pubs_files.append(f)

        DB_CON.commit()
        # print('Los archivos modificados fueron registrados en %s' % (db_properties['f_table'],))

    except mysql.connector.Error as err:
        print("Error al intentar modificar la tabla. Código de error: %d. ROLLBACK" % (err,))
        DB_CON.rollback()
        pubs_files.clear()

    else:
        db_cur.close()

    finally:
        return pubs_files

def changePubAndNotify(FILE_LIST, DB_CON):
    """Given a LIST OF PUBLIC FILES change their visibility to PRIVATE, make changes on the Database
    and Comunicate the owners via email.

    :param FILE_LIST: list of files on Google Drive's API format.
    :param DB_CON: connection instance on database.
    """

    #FIRST: Register all the PUBLIC files found on the file public history table
    try:
        DB_CON.autocommit = False
        db_cur =DB_CON.cursor()

        for PUB_FOUND in FILE_LIST:

            owner = getFileOwner(PUB_FOUND)

            insert_query = "INSERT INTO %s (id, name, extention, owner, foundTime, trashed, ownedByMe) " \
                           "VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s);" % (db_properties['p_h_table'],
                                                                               PUB_FOUND['id'],
                                                                               PUB_FOUND['name'],
                                                                               mime_type_dic[PUB_FOUND['mimeType']],
                                                                               owner,
                                                                               current_run_time,
                                                                               PUB_FOUND['trashed'],
                                                                               PUB_FOUND['ownedByMe'])
            # print('atempt: ' + insert_query)
            db_cur.execute(insert_query)

        DB_CON.commit()
        # print('Los archivos que eran publicos fueron registrados')

    except mysql.connector.Error as err:
        print("Error al intentar agregar en la tabla. Código de error: %s. ROLLBACK" %str(err))
        DB_CON.rollback()

    else:
        db_cur.close()

    succed_CRQ_list = list()

    #SECOND: Try to modify de visibility to PRIVATE on the DRIVE
    for CRQ in FILE_LIST:
        if removePermission(drive_service, CRQ['id'], 'anyone'):
            succed_CRQ_list.append(CRQ) #if the change request failed, discard file

    #THIRD: Update the files visibility on the files table
    try:
        DB_CON.autocommit = False
        db_cur = DB_CON.cursor()

        for CRQ in succed_CRQ_list:

            update_query = "UPDATE %s SET public = False WHERE id LIKE '%s'" %(db_properties['f_table'],
                                                                               CRQ['id'])

            # print('atempt: ' + update_query)
            db_cur.execute(update_query)

        DB_CON.commit()
        # print('Los archivos que eran publicos fueron modificados')

    except mysql.connector.Error as err:
        print("Error al intentar modificar la tabla. Código de error: %d. ROLLBACK" %(err))
        DB_CON.rollback()

    else:
        db_cur.close()

    #Fourth: Communicate the changes via email to their owners
    for CD in succed_CRQ_list:
        notifyPubChangeByEmail(mail_service, CD)



def Main():

    parser = argparse.ArgumentParser(description="This program communicates with MySQL Server and Google Drive."
                                                 "It will modify the files and folders visibility of Google Drive's"
                                                 " account (login will be required). It will also drop tables "
                                                 "in order to register the files status of the Google Drive logged in.")
    requiredArgs = parser.add_argument_group('Required arguments')
    requiredArgs.add_argument('localhost', help='MySQL LocalHost name.', action="store")
    requiredArgs.add_argument('database', help='MySQL DataBase name.', action="store")
    requiredArgs.add_argument('user', help='MySQL User name.', action="store")
    parser.add_argument('-p', '--password', help='MySQL Password.', default='', action="store")

    args = parser.parse_args()
    db_properties['host'] = args.localhost
    db_properties['database'] = args.database
    db_properties['user'] = args.user
    db_properties['password'] = args.password

    response = drive_service.about().get(fields='user').execute()

    r = response.get('user')
    myEmail = str(r['emailAddress'])
    u_name = myEmail.split('@')[0]

    db_properties['f_table'] = u_name + '_f_t' #Sets user file table's name
    db_properties['p_h_table'] = u_name + '_p_h_t' #Sets user public history table's name


    dbConectionInstance = customMySql.customMySql(db_properties)
    db_connection = dbConectionInstance.createDbConnection()
    dbConectionInstance.dbInit(db_connection)
    print("\n\t\t\t¡¡¡ Bienvenide %s !!! \n\nEn este momento estamos evaluando el contenido de su Google Drive"
              " y cambiaremos los archivos que tenga compartidos como Públicos a Privados.\nEn tal caso "
              "le estaremos comunicando por email lo sucedido. Sea paciente por favor.\n"%u_name)

    last_run_time = getLastRunTime(config_file)

    saveCurrentRunTime(config_file, current_run_time)


    # the following query will discard all files that haven't been modified since last run
    query = "modifiedTime >= '"+last_run_time+"'"
    page_token = None

    new_files_list = list()
    old_files_list = list()
    pub_files_list = list()
    while True:
        response = drive_service.files().list(q=query, pageSize= 1000,spaces='drive',
                                              fields="nextPageToken, files(id, name, mimeType, "
                                                     "createdTime, modifiedTime, shared, trashed, "
                                                     "ownedByMe, owners, permissions)",
                                              pageToken=page_token).execute()

        new_files_list.clear()
        old_files_list.clear()
        pub_files_list.clear()
        for file in response.get('files', []):
            if last_run_time > file.get('createdTime'):
                old_files_list.append(file)
            else:
                new_files_list.append(file)

            page_token = response.get('nextPageToken', None)

        pub_files_list.extend(insertNewFilesAndReturnPubs(new_files_list, db_connection))
        pub_files_list.extend(updateOldFilesAndReturnPubs(old_files_list, db_connection))
        changePubAndNotify(pub_files_list, db_connection)

        if page_token is None:
            break

    if db_connection.is_connected():
        db_connection.close()
        # print("Se ha finalizado la conexión a la Base de Datos.")
    print("\n\t\t\t\tTenga Ud. un buen día :)\n")
    return 0

if __name__ == '__main__':
    Main()