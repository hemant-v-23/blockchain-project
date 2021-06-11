from flask import Flask ,render_template, redirect, url_for, request
import csv
import ipfshttpclient
from web3 import Web3
import pandas as pd
import os

PRH,HRH,MRH,PHH,PMH,PRAR="","","","","",""

def upload_files():
    client=ipfshttpclient.connect('/dns4/ipfs.infura.io/tcp/5001/https')
    A=client.add('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Registry.csv')
    d=dict(A)
    global PRH
    PRH=d.get('Hash')
    B=client.add('C:\\Users\Akshay\Pictures\Blockchain-project\\Hospital-Registry.csv')
    d=dict(B)
    global HRH
    HRH=d.get('Hash')
    C=client.add('C:\\Users\Akshay\Pictures\Blockchain-project\\Medical-Registry.csv')
    d=dict(C)
    global MRH
    MRH=d.get('Hash')
    D=client.add('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Hospital.csv')
    d=dict(D)
    global PHH
    PHH=d.get('Hash')
    E=client.add('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Medical.csv')
    d=dict(E)
    global PMH
    PMH=d.get('Hash')
    F=client.add('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv')
    d=dict(F)
    global PRAR
    PRAR=d.get('Hash')

def transaction():
    ganache="HTTP://127.0.0.1:7545"
    web3=Web3(Web3.HTTPProvider(ganache))
    if web3.isConnected()==True:

        account1="0x76d0A841530DA038721f813D938CE5b995dB54B2"
        account2="0x00d0e1797F5699fAbe148D08438D2a7370aD0f33"
        pk="1b3b2efd00a314a460b1f0c666bace146e16787b7d5e9eb96f8d7f5775c94ea8"

        nonce=web3.eth.getTransactionCount(account1)
        d={"nonce":nonce,'to':account2,'value':web3.toWei(1,'ether'),'gas':2000000,'gasPrice':web3.toWei('50','gwei')}

        sign=web3.eth.account.signTransaction(d,pk)
        hash=web3.eth.sendRawTransaction(sign.rawTransaction)
        ans=web3.toHex(hash)
        return ans
    else:
        return "No transaction made"

app=Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/patient-login", methods=['POST','GET'])
def patient_login():
    if request.method == "POST":
        user=request.form["uname"]
        file=open('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Registry.csv')
        read=csv.reader(file)
        flag=True
        for i in read:
            if user==i[0]:
                return render_template("patient.html")
        if flag:
            return f"<h1>Login unsuccessfull</h1>"
    else:
        return render_template("login.html")

@app.route("/book_an_appointment", methods=['POST','GET'])
def book_an_appointment():
    if request.method == "POST":
        user=request.form["data"]
        global PHH
        client=ipfshttpclient.connect('/dns4/ipfs.infura.io/tcp/5001/https')
        getfile=client.cat(PHH)
        ans=getfile.decode('utf-8')
        ans="".join(ans)
        file=open('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Hospital.csv','w')
        file.write(ans)
        file.close()
        if os.stat('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Hospital.csv').st_size!=0:
            ans=pd.read_csv('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Hospital.csv')
            ans.to_csv('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Hospital.csv',index=False)

        file=open('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Hospital.csv','a',newline="")
        write=csv.writer(file)
        write.writerow(["Booked Appointment details "+user+" ",transaction()])
        file.close()

        D=client.add('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Hospital.csv')
        d=dict(D)
        PHH=d.get('Hash')
        return redirect(url_for("successfull", input=PHH))

    else:
        return render_template("book.html")

@app.route("/search_medicine", methods=['POST','GET'])
def search_medicine():
    if request.method == "POST":
        user=request.form["data"]
        global PMH
        client=ipfshttpclient.connect('/dns4/ipfs.infura.io/tcp/5001/https')
        getfile=client.cat(PMH)
        ans=getfile.decode('utf-8')
        ans="".join(ans)
        file=open('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Medical.csv','w')
        file.write(ans)
        file.close()
        if os.stat('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Medical.csv').st_size!=0:
            ans=pd.read_csv('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Medical.csv')
            ans.to_csv('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Medical.csv',index=False)

        file=open('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Medical.csv','a',newline="")
        write=csv.writer(file)
        write.writerow(["Requested medicine info "+user,transaction()])
        file.close()

        D=client.add('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Medical.csv')
        d=dict(D)
        PMH=d.get('Hash')

        return redirect(url_for("successfull", input=PMH))
    else:
        return render_template("search.html")


@app.route("/PRAR")
def PRAR():
    return render_template("PRAR.html")

@app.route("/hospital-login", methods=['POST','GET'])
def hospital_login():
    if request.method == "POST":
        user=request.form["uname"]
        file=open('C:\\Users\Akshay\Pictures\Blockchain-project\\Hospital-Registry.csv')
        read=csv.reader(file)
        flag=True
        for i in read:
            if user==i[0]:
                return render_template("hospital.html")
        if flag:
            return f"<h1>Login unsuccessfull</h1>"
    else:
        return render_template("login.html")

@app.route("/HRAR", methods=['POST','GET'])
def HRAR():
    if request.method == "POST":
        user=request.form["data"]
        global PRAR
        client=ipfshttpclient.connect('/dns4/ipfs.infura.io/tcp/5001/https')
        getfile=client.cat(PRAR)
        ans=getfile.decode('utf-8')
        ans="".join(ans)
        file=open('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv','w')
        file.write(ans)
        file.close()
        if os.stat('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv').st_size!=0:
            ans=pd.read_csv('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv')
            ans.to_csv('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv',index=False)

        file=open('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv','a',newline="")
        write=csv.writer(file)
        h=["Requested appointment from "+user+" is confirmed ",transaction()]
        write.writerow(h)
        file.close()
        D=client.add('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv')
        d=dict(D)
        PRAR=d.get('Hash')
        return redirect(url_for("successfull", input=PRAR))
    else:
        return render_template("HRAR.html")

@app.route("/medical-login", methods=['POST','GET'])
def medical_login():
    if request.method == "POST":
        user=request.form["uname"]
        file=open('C:\\Users\Akshay\Pictures\Blockchain-project\\Medical-Registry.csv')
        read=csv.reader(file)
        flag=True
        for i in read:
            if user==i[0]:
                return render_template("medical.html")
        if flag:
            return f"<h1>Login unsuccessfull</h1>"
    else:
        return render_template("login.html")

@app.route("/MRAR", methods=['POST','GET'])
def MRAR():
    if request.method == "POST":
        user=request.form["data"]
        global PRAR
        client=ipfshttpclient.connect('/dns4/ipfs.infura.io/tcp/5001/https')
        getfile=client.cat(PRAR)
        ans=getfile.decode('utf-8')
        ans="".join(ans)
        file=open('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv','w')
        file.write(ans)
        file.close()
        if os.stat('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv').st_size!=0:
            ans=pd.read_csv('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv')
            ans.to_csv('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv',index=False)

        file=open('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv','a',newline="")
        write=csv.writer(file)
        h=["Requested Medicine from "+user+" is confirmed ",transaction()]
        write.writerow(h)
        file.close()
        D=client.add('C:\\Users\Akshay\Pictures\Blockchain-project\\Patient-Request-And-Reply.csv')
        d=dict(D)
        PRAR=d.get('Hash')
        return redirect(url_for("successfull", input=PRAR))
    else:
        return render_template("HRAR.html")

@app.route("/<input>")
def successfull(input):
    url="http://127.0.0.1:5001/ipfs/bafybeif4zkmu7qdhkpf3pnhwxipylqleof7rl6ojbe7mq3fzogz6m4xk3i/#/ipfs/"+str(input)
    return f"<h1>Transaction successfull</h1><a href=\"home\">home</a><br/><br>"+url

if __name__=="__main__":
    upload_files()
    app.run(debug=True)
