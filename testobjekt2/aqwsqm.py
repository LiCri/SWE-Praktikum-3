# coding=utf-8

#------------------------------------------------------------------------------
# Import
#------------------------------------------------------------------------------

import string
import re

import sys

"""
Verwaltung der Generierung von SQL-Statements fuer Queries
"""

#------------------------------------------------------------------------------
class SQLStmtManager_cl(object):
#------------------------------------------------------------------------------

   #---------------------------------------------------------------------------
   def __init__(self, FileName_spl):
   #---------------------------------------------------------------------------

      self.StmtDefs_o = {}
      # Datei mit Konfigurationsdaten einlesen
      try:
         File_o = open(FileName_spl, "rU")
         try:
            Buffer_s = File_o.read()
            self.StmtDefs_o = eval(Buffer_s)
         except:
            print("[SQLStmtManager][init] eval-Fehler : ", sys.exc_info()[2])
         finally:
            File_o.close()
      except:
         pass

      self.StmtObjects_o = {}
      # die Stmt-Objekte erzeugen
      for Key_s in self.StmtDefs_o:
         if Key_s[0:6] == 'Select':
            self.StmtObjects_o[Key_s] = SelectStatement_cl(self.StmtDefs_o[Key_s])
         elif Key_s[0:6] == 'Update':
            self.StmtObjects_o[Key_s] = UpdateStatement_cl(self.StmtDefs_o[Key_s])
         elif Key_s[0:6] == 'Insert':
            self.StmtObjects_o[Key_s] = InsertStatement_cl(self.StmtDefs_o[Key_s])
         elif Key_s[0:6] == 'Delete':
            self.StmtObjects_o[Key_s] = DeleteStatement_cl(self.StmtDefs_o[Key_s])

   #---------------------------------------------------------------------------
   def GenStatement_px(self, QueryName_spl, QueryVars_dpl):
   #---------------------------------------------------------------------------
      """
      - Statement-Definition anhand des Namens ermitteln
      - dann die Generierung der Anweisung durchfuehren
      """
      Cmd_s = None
      if QueryName_spl in self.StmtObjects_o:
         SQLStmtObject_o = self.StmtObjects_o[QueryName_spl]
         Cmd_s = SQLStmtObject_o.Generate_px(QueryVars_dpl)

      return Cmd_s

#------------------------------------------------------------------------------
class SQLStatement_cl(object):
#------------------------------------------------------------------------------

   #---------------------------------------------------------------------------
   def __init__(self, Definition_opl):
   #---------------------------------------------------------------------------
      pass

   #---------------------------------------------------------------------------
   def Generate_px(self, QueryVars_dpl):
   #---------------------------------------------------------------------------
      pass

#------------------------------------------------------------------------------
class SelectStatement_cl(SQLStatement_cl):
#------------------------------------------------------------------------------
   """
   Zugriff auf ein einzelnes Objekt (= Record) per OID
   """
   #---------------------------------------------------------------------------
   def __init__(self, Definition_opl):
   #---------------------------------------------------------------------------
      """
      Aufbau der Definition (Beispiel)

   ,"SelectInst" :
    {
        "MainTable"     : "institutionen_tb i"
       ,"MainIdField_s" : "i.oid_i"
       ,"ResultSet"     : # hier nur weitere Felder eintragen
        {
            "Fields"     : [
                            "i.bezeichnung_s"
                           ,"i.bezeichnungdetail1_s"
                           ,"i.bezeichnungdetail2_s"
                           ,"i.strasse_s"
                           ,"i.hausnummer_s"
                           ,"i.plz_s"
                           ,"i.ort_s"
                           ,"wk1.wert_s as region_s"
                           ,"wk2.wert_s as land_s"
                           ]
           ,"Joins"      : [ "left outer join wertekataloge_tb wk1 on b.wkregion_i = wk1.wk_i"
                            ,"left outer join wertekataloge_tb wk2 on b.wkland_i = wk2.wk_i"]
        }
      """
      self.MainTable_s    = Definition_opl["MainTable"]
      self.MainIdField_s  = Definition_opl["MainIdField_s"]
      self.ResultSet_o    = Definition_opl["ResultSet"]

      # FilterFields auswerten : Tabellen und Joins zusammenfassen

      self.FilterTables_o = [self.MainTable_s]
      self.FilterJoins_o  = self.ResultSet_o['Joins']

   #---------------------------------------------------------------------------
   def Generate_px(self, QueryVars_dpl):
   #---------------------------------------------------------------------------
      """
      es muss sichergestellt werden, dass die QueryVar OID existiert (mit Integer-Wert)
      """
      Cmd_s = None
      if "OID" in QueryVars_dpl:
         Cmd_s = "select " + self.MainIdField_s

         # Felder des Resultset eintragen
         for Key_s in self.ResultSet_o["Fields"]:
            Cmd_s += "," + Key_s

         # Main-Table eintragen
         Cmd_s += " from " + self.MainTable_s

         # Joins eintragen
         for Key_s in self.ResultSet_o["Joins"]:
            if Key_s != "":
               Cmd_s += " " + Key_s

         # Where-Klausel eintragen mit Subselect

         Cmd_s += " where " + self.MainIdField_s + " = "  + str(QueryVars_dpl["OID"])

      return Cmd_s

#------------------------------------------------------------------------------
class UpdateStatement_cl(SQLStatement_cl):
#------------------------------------------------------------------------------
   """
   einzelnes Objekt (= Record) per OID + Daten aktualisieren
   """
   #---------------------------------------------------------------------------
   def __init__(self, Definition_opl):
   #---------------------------------------------------------------------------
      """
      Aufbau der Definition (Beispiel)

   ,"UpdateInst" :
    {
        "MainTable"     : "institutionen_tb i"
       ,"MainIdField_s" : "i.oid_i"
       ,"Fields"        : [
                            "i.bezeichnung_s"
                           ,"i.bezeichnungdetail1_s"
                           ,"i.bezeichnungdetail2_s"
                           ,"i.strasse_s"
                           ,"i.hausnummer_s"
                           ,"i.plz_s"
                           ,"i.ort_s"
                           ,"i.wkregion_i
                           ,"i.wkland_i
                           ]
       ,"Values"        : ["%s", "%s", "%s", "%s", "%s", "%s", "%s", NULL, NULL]
    }
      """
      self.MainTable_s    = Definition_opl["MainTable"]
      self.MainIdField_s  = Definition_opl["MainIdField_s"]
      self.Fields_a       = Definition_opl["Fields"]
      self.ValueFormats_a = Definition_opl["Values"]

      # Alias-Prefix vor den Feldnamen entfernen, falls vorhanden
      for loop_i in range(0,len(self.Fields_a)):
         Parts_a = self.Fields_a[loop_i].split('.')
         if len(Parts_a) > 1:
            self.Fields_a[loop_i] = Parts_a[1]

   #---------------------------------------------------------------------------
   def Generate_px(self, QueryVars_dpl):
   #---------------------------------------------------------------------------
      """
      es muss sichergestellt werden, dass die QueryVar OID existiert (mit Integer-Wert)
      """
      Cmd_s = None
      if "OID" in QueryVars_dpl:
         Cmd_s = "update " + self.MainTable_s + " set "

         # Felder eintragen
         loop_i = 0
         for Key_s in self.Fields_a:
            if loop_i > 0:
               Cmd_s += ","
            if Key_s in QueryVars_dpl:
               # Wert formatieren
               if self.ValueFormats_a[loop_i] == None:
                  Value_s = "NULL"
               else:
                  # Datentyp anhand des Postfix auswerten
                  if Key_s[-2:] == '_s':
                     # String
                     Value_s = self.ValueFormats_a[loop_i] % QueryVars_dpl[Key_s]
                  else:
                     # alle anderen, insbesondere Integer
                     if QueryVars_dpl[Key_s] == '':
                        # als NULL-Wert interpretieren
                        Value_s = 'NULL'
                     else:
                        Value_s = self.ValueFormats_a[loop_i] % QueryVars_dpl[Key_s]
                  # bisher nur : Value_s = self.ValueFormats_a[loop_i] % QueryVars_dpl[Key_s]
               Cmd_s += Key_s + ' = ' + Value_s
            else:
               # keine Angabe, daher NULL-Value eintragen
               Cmd_s += Key_s + ' = NULL '
            loop_i += 1

         # Where-Klausel eintragen

         Cmd_s += " where " + self.MainIdField_s + " = "  + str(QueryVars_dpl["OID"])

      return Cmd_s

#------------------------------------------------------------------------------
class InsertStatement_cl(SQLStatement_cl):
#------------------------------------------------------------------------------
   """
   einzelnes Objekt (= Record) per OID + Daten aktualisieren
   """
   #---------------------------------------------------------------------------
   def __init__(self, Definition_opl):
   #---------------------------------------------------------------------------
      """
      Aufbau der Definition (Beispiel)

   ,"InsertInst" :
    {
        "MainTable"     : "institutionen_tb i"
       ,"MainIdField_s" : "i.oid_i"
       ,"Fields"        : [
                            "i.bezeichnung_s"
                           ,"i.bezeichnungdetail1_s"
                           ,"i.bezeichnungdetail2_s"
                           ,"i.strasse_s"
                           ,"i.hausnummer_s"
                           ,"i.plz_s"
                           ,"i.ort_s"
                           ,"i.wkregion_i"
                           ,"i.wkland_i"
                           ]
       ,"Values"        : ["'%s'", "'%s'", "'%s'", "'%s'", "'%s'", "'%s'", "'%s'", None, None]
    }
      """
      self.MainTable_s    = Definition_opl["MainTable"]
      self.MainIdField_s  = Definition_opl["MainIdField_s"]
      self.Fields_a       = Definition_opl["Fields"]
      self.ValueFormats_a = Definition_opl["Values"]

      # Alias-Prefix vor den Feldnamen entfernen, falls vorhanden
      for loop_i in range(0,len(self.Fields_a)):
         Parts_a = self.Fields_a[loop_i].split('.')
         if len(Parts_a) > 1:
            self.Fields_a[loop_i] = Parts_a[1]


   #---------------------------------------------------------------------------
   def Generate_px(self, QueryVars_dpl):
   #---------------------------------------------------------------------------

      Cmd_s = "insert into " + self.MainTable_s + "("

      # Felder eintragen
      for loop_i in range(0,len(self.Fields_a)):
         if loop_i > 0:
            Cmd_s += ","
         Cmd_s += self.Fields_a[loop_i]

      Cmd_s += ') values ('

      # Werte eintragen
      loop_i = 0
      for Key_s in self.Fields_a:
         if loop_i > 0:
            Cmd_s += ","
         if Key_s in QueryVars_dpl:
            # Wert formatieren
            if self.ValueFormats_a[loop_i] == None:
               Value_s = "NULL"
            else:
               # Datentyp anhand des Postfix auswerten
               if Key_s[-2:] == '_s':
                  # String
                  Value_s = self.ValueFormats_a[loop_i] % QueryVars_dpl[Key_s]
               else:
                  # alle anderen, insbesondere Integer
                  if QueryVars_dpl[Key_s] == '':
                     # als NULL-Wert interpretieren
                     Value_s = 'NULL'
                  else:
                     Value_s = self.ValueFormats_a[loop_i] % QueryVars_dpl[Key_s]
                     
            Cmd_s += Value_s
         else:
            # keine Angabe, daher NULL-Value eintragen
            Cmd_s += 'NULL '

         loop_i += 1

      Cmd_s += ')'

      return Cmd_s

#------------------------------------------------------------------------------
class DeleteStatement_cl(SQLStatement_cl):
#------------------------------------------------------------------------------
   """
   einzelnes Objekt (= Record) per OID entfernen
   """
   #---------------------------------------------------------------------------
   def __init__(self, Definition_opl):
   #---------------------------------------------------------------------------
      """
      Aufbau der Definition (Beispiel)

   ,"DeleteInst" :
    {
        "MainTable"     : "institutionen_tb i"
       ,"MainIdField_s" : "i.oid_i"
    }
      """
      self.MainTable_s    = Definition_opl["MainTable"]
      self.MainIdField_s  = Definition_opl["MainIdField_s"]

   #---------------------------------------------------------------------------
   def Generate_px(self, QueryVars_dpl):
   #---------------------------------------------------------------------------
      """
      es muss sichergestellt werden, dass die QueryVar OID existiert (mit Integer-Wert)
      """
      Cmd_s = None
      if "OID" in QueryVars_dpl:
         Cmd_s = "delete from " + self.MainTable_s + " where " + self.MainIdField_s + " = " + str(QueryVars_dpl["OID"])

      return Cmd_s

#------------------------------------------------------------------------------
# Testumgebung
#------------------------------------------------------------------------------
if __name__ == '__main__':
#------------------------------------------------------------------------------
   SQLStmtManager_o = SQLStmtManager_cl("sql.cfg")

   Query_s = SQLStmtManager_o.GenStatement_px("SelectInst", {"OID":4711, "bauwerk_ort_s":"Bochum", "kuenstler_name_s":"A"})
   print(Query_s)

   Query_s = SQLStmtManager_o.GenStatement_px("UpdateInst", {"OID":4711, "bezeichnung_s":"xyz", "ort_s":"Heimat"})
   print(Query_s)

   Query_s = SQLStmtManager_o.GenStatement_px("InsertInst", {"OID":4711, "bezeichnung_s":"xyz", "ort_s":"Heimat"})
   print(Query_s)

   Query_s = SQLStmtManager_o.GenStatement_px("DeleteInst", {"OID":4711})
   print(Query_s)

# EOF
