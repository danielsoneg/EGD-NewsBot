# -*- coding: utf-8 -*-
import hashlib
import binascii
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

from auth import EVERNOTE as EVAUTH

class Evernote(object):
  def __init__(self):
    evernoteHost = "sandbox.evernote.com"
    userStoreUri = "https://" + evernoteHost + "/edam/user"
    userStoreHttpClient = THttpClient.THttpClient(userStoreUri)
    userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
    userStore = UserStore.Client(userStoreProtocol)
    noteStoreUrl = userStore.getNoteStoreUrl(EVAUTH)
    noteStoreHttpClient = THttpClient.THttpClient(noteStoreUrl)
    noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
    self.noteStore = NoteStore.Client(noteStoreProtocol)

  def makeNote(self, title, body, url):
    note = Types.Note()
    note.title = title
    note.content = body
    attributes = Types.NoteAttributes()
    attributes.sourceURL = url
    note.attributes = attributes
    
    createdNote = self.noteStore.createNote(EVAUTH, note)
    return createdNote
