#imports
import mysql.connector as conn
import pandas as pd

    #vars
class mydb:

    def __init__(self):
        self.userVar = "root"
        self.pwdVar = "mysql"
        self.connection = True
        self.con = None
        self.details()

    #funcs
    def details(self, c = True, a = "root",b = "mysql"): #grabbing details
        self.uservar, self.pwdVar, self.connection = str(a), str(b), c
        self.con = conn.connect(host = "localhost", user = self.userVar, password = self.pwdVar)
        self.beginning()

    def beginning(self):    #initialise database and reading
        op = self.con.cursor()
        op.execute("create database if not exists cse3001")
        op.execute("use cse3001")
        op.execute("show tables")
        if len(op.fetchall()) == 2:
            #no need to recreate tables
            return

        self.reupdate() #if not 2 tables

    def reupdate(self):
        op = self.con.cursor()
        op.execute("drop table if exists reactions")
        op.execute("drop table if exists weights")

        op.execute("create table if not exists weights(name varchar(50) primary key, weight float)")
        weights = pd.read_csv("weights1.csv").to_dict("index")
        query = "insert into weights values('{}', {})"
        for i in weights:
            op.execute(query.format(weights[i]["name"], weights[i]["weight"]))
            
        op.execute("create table if not exists reactions(id integer primary key, reagent1 varchar(50) not null, count1 integer,\
            reagent2 varchar(50) not null, count2 integer, product varchar(50) not null, count3 integer, conditions text, extra text,\
                foreign key(reagent1) references weights(name), foreign key(reagent2) references weights(name),\
                    foreign key(product) references weights(name))")
        reactions = pd.read_csv("reactions1.csv").to_dict("index")
        query = "insert into reactions values({}, '{}', {}, '{}', {}, '{}', {}, '{}', '{}')"
        for i in reactions:
            op.execute(query.format(reactions[i]["ID"], reactions[i]["reactant1"], reactions[i]["count1"], reactions[i]["reactant2"], 
                reactions[i]["count2"], reactions[i]["product"], reactions[i]["count3"], reactions[i]["conditions"], reactions[i]["extra"]))
                
        op.execute("commit")


    def getall(self):
        lst = []
        op = self.con.cursor()
        op.execute("select distinct(reagent1) from reactions")
        lst.append([ str(x[0]) for x in list( op.fetchall() ) ])
        op.execute("select distinct(reagent2) from reactions")
        lst.append([ str(x[0]) for x in list( op.fetchall() ) ])
        op.execute("select distinct(product) from reactions")
        lst.append([ str(x[0]) for x in list( op.fetchall() ) ])
        return lst

    def getOne(self, boxNo, value):
        op = self.con.cursor()
        if boxNo == 1:
            op.execute("select distinct(reagent2) from reactions where reagent1 = '{}'".format(value))
            lst1 = [x[0] for x in op.fetchall()]
            op.execute("select distinct(product) from reactions where reagent1 = '{}'".format(value))
            lst2 = [x[0] for x in op.fetchall()]
        elif boxNo == 2:
            op.execute("select distinct(reagent1) from reactions where reagent2 = '{}'".format(value))
            lst1 = [x[0] for x in op.fetchall()]
            op.execute("select distinct(product) from reactions where reagent2 = '{}'".format(value))
            lst2 = [x[0] for x in op.fetchall()]
        elif boxNo == 3:
            op.execute("select distinct(reagent1) from reactions where product = '{}'".format(value))
            lst1 = [x[0] for x in op.fetchall()]
            op.execute("select distinct(reagent2) from reactions where product = '{}'".format(value))
            lst2 = [x[0] for x in op.fetchall()]
        return lst1, lst2

    def getTwo(self, firstBoxNo, secondBoxNo, firstValue, secondValue):
        op = self.con.cursor()
        if firstBoxNo == 1:
            if secondBoxNo == 2: #1,2
                op.execute("select product from reactions where reagent1 = '{}' and reagent2 = '{}'".format(firstValue, secondValue))
                ret1 = op.fetchall()[0][0]
                op.execute("select extra from reactions where reagent1 = '{}' and reagent2 = '{}'".format(firstValue, secondValue))
                ret2 = op.fetchall()[0][0]
                op.execute("select conditions from reactions where reagent1 = '{}' and reagent2 = '{}'".format(firstValue, secondValue))
                ret3 = op.fetchall()[0][0]
                ret4 = []
                op.execute("select weight from weights where name = '{}'".format(firstValue))
                ret4.append(op.fetchall()[0][0])
                op.execute("select weight from weights where name = '{}'".format(secondValue))
                ret4.append(op.fetchall()[0][0])
                op.execute("select weight from weights where name = '{}'".format(ret1))
                ret4.append(op.fetchall()[0][0])
            elif secondBoxNo == 3: #1,3
                op.execute("select reagent2 from reactions where reagent1 = '{}' and product = '{}'".format(firstValue, secondValue))
                ret1 = op.fetchall()[0][0]
                op.execute("select extra from reactions where reagent1 = '{}' and product = '{}'".format(firstValue, secondValue))
                ret2 = op.fetchall()[0][0]
                op.execute("select conditions from reactions where reagent1 = '{}' and product = '{}'".format(firstValue, secondValue))
                ret3 = op.fetchall()[0][0]
                ret4 = []
                op.execute("select weight from weights where name = '{}'".format(firstValue))
                ret4.append(op.fetchall()[0][0])
                op.execute("select weight from weights where name = '{}'".format(ret1))
                ret4.append(op.fetchall()[0][0])
                op.execute("select weight from weights where name = '{}'".format(secondValue))
                ret4.append(op.fetchall()[0][0])

        elif firstBoxNo == 2:  #2, 3
            op.execute("select reagent1 from reactions where reagent2 = '{}' and product = '{}'".format(firstValue, secondValue))
            ret1 = op.fetchall()[0][0]
            op.execute("select extra from reactions where reagent2 = '{}' and product = '{}'".format(firstValue, secondValue))
            ret2 = op.fetchall()[0][0]
            op.execute("select conditions from reactions where reagent2 = '{}' and product = '{}'".format(firstValue, secondValue))
            ret3 = op.fetchall()[0][0]
            ret4 = []
            op.execute("select weight from weights where name = '{}'".format(ret1))
            ret4.append(op.fetchall()[0][0])
            op.execute("select weight from weights where name = '{}'".format(firstValue))
            ret4.append(op.fetchall()[0][0])
            op.execute("select weight from weights where name = '{}'".format(secondValue))
            ret4.append(op.fetchall()[0][0])
        return ret1, ret2, ret3, ret4 #third missing value, extra info, conditions, [weight1, weight2, weight3]
