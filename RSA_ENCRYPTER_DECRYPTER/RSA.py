import tkinter as tk
#import PyPDF2
#import tkinter as tk
from PIL import Image, ImageTk
import os
root=tk.Tk()
root.tk.call('encoding','system','utf-8')
root.configure(background='white')
root.title('  My First Project in Python')
root.iconbitmap('logo.ico')
root.geometry("910x700")

name_var=tk.StringVar()
key_var=tk.IntVar()
encrypt_btn=tk.StringVar()
decrypt_btn=tk.StringVar()
message_var=tk.StringVar()
choose_var=tk.IntVar()
encryption_btn=tk.StringVar()
decryption_btn=tk.StringVar()

logo=Image.open('front.png').resize((500,250))
logo=ImageTk.PhotoImage(logo)
logo_label=tk.Label(image=logo,borderwidth=0)
logo_label.image=logo
logo_label.grid(row=0,column=0,columnspan=2,pady=1)

instructions=tk.Label(root, text="Select a File on your computer to Encrypt/Decrypt", font="Raleway",background="#eee",width=100)
instructions.grid(row=1,column=0,columnspan=2,pady=20)

name_label = tk.Label(root,text='Enter File Path --',width=20,background="white").grid(row=2,column=0,pady=10)
name_entry=tk.Entry(root,textvariable=name_var,width=80,background="#eee").grid(row=2,column=1,pady=10)

key_label = tk.Label(root,text='Enter the Key --',width=20,background="white").grid(row=3,column=0,pady=10)
key_entry=tk.Entry(root,textvariable=key_var,width=80,background="#eee").grid(row=3,column=1,pady=10)

def encrypt():
    # try block to handle exception
    try:
    	path = name_var.get()
    	# taking encryption key as input
    	key = key_var.get()
    	
    	# print path of file and encryption key that
    	# we are using
    	print('The path of file : ', path)
    	print('Key for encryption : ', key)
    	
    	# open file for reading purpose
    	fin = open(path, 'rb')
    	
    	# storing file data in variable "file"
    	file = fin.read()
    	fin.close()
    	
    	# converting file into byte array to
    	# perform encryption easily on numeric data
    	file = bytearray(file)
    
    	# performing XOR operation on each value of bytearray
    	for index, values in enumerate(file):
    		file[index] = values ^ key
    
    	# opening file for writing purpose
    	fin = open(path, 'wb')
    	
    	# writing encrypted data in file
    	fin.write(file)
    	fin.close()
    	encrypt_btn.set("Encrypted")
    
    	
    except Exception:
    	print('Error caught : ', Exception.__name__)
        
def decrypt():
    # try block to handle the exception
    try:
    	# take path of file as a input
    	path = name_var.get()
    	
    	# taking decryption key as input
    	key = key_var.get()
    	
    	# print path of file and decryption key that we are using
    	print('The path of file : ', path)
    	print('Note : Encryption key and Decryption key must be same.')
    	print('Key for Decryption : ', key)
    	
    	# open file for reading purpose
    	fin = open(path, 'rb')
    	
    	# storing file data in variable "file"
    	file = fin.read()
    	fin.close()
    	
    	# converting file into byte array to perform decryption easily on numeric data
    	file = bytearray(file)
    
    	# performing XOR operation on each value of bytearray
    	for index, values in enumerate(file):
    		file[index] = values ^ key
    
    	# opening file for writing purpose
    	fin = open(path, 'wb')
    	
    	# writing decryption data in file
    	fin.write(file)
    	fin.close()
    	decrypt_btn.set("Decrypted")
    
    
    except Exception:
    	print('Error caught : ', Exception.__name__)


#RSA ALGORITHM STARTING
# STEP 1: Generate Two Large Prime Numbers (p,q) randomly
from random import randrange, getrandbits


def power(a,d,n):
  ans=1;
  while d!=0:
    if d%2==1:
      ans=((ans%n)*(a%n))%n
    a=((a%n)*(a%n))%n
    d>>=1
  return ans;


def MillerRabin(N,d):
  a = randrange(2, N - 1)
  x=power(a,d,N);
  if x==1 or x==N-1:
    return True;
  else:
    while(d!=N-1):
      x=((x%N)*(x%N))%N;
      if x==1:
        return False;
      if x==N-1:
        return True;
      d<<=1;
  return False;


def is_prime(N,K):
  if N==3 or N==2:
    return True;
  if N<=1 or N%2==0:
    return False;
  
  #Find d such that d*(2^r)=X-1
  d=N-1
  while d%2!=0:
    d/=2;

  for _ in range(K):
    if not MillerRabin(N,d):
      return False;
  return True;  
  



def generate_prime_candidate(length):
  # generate random bits
  p = getrandbits(length)
  # apply a mask to set MSB and LSB to 1
  # Set MSB to 1 to make sure we have a Number of 1024 bits.
  # Set LSB to 1 to make sure we get a Odd Number.
  p |= (1 << length - 1) | 1
  return p



def generatePrimeNumber(length):
  A=4
  while not is_prime(A, 128):
        A = generate_prime_candidate(length)
  return A



length=5
P=generatePrimeNumber(length)
Q=generatePrimeNumber(length)

#Step 2: Calculate N=P*Q
N=P*Q

#Step 3: Calculate Euler Totient Function = (P-1)*(Q-1)
eulerTotient=(P-1)*(Q-1)

#Step 4: Find E such that GCD(E,eulerTotient)=1(i.e., e should be co-prime) such that it satisfies this condition:-  1<E<eulerTotient

def GCD(a,b):
  if a==0:
    return b;
  return GCD(b%a,a)

E=generatePrimeNumber(4)
while GCD(E,eulerTotient)!=1:
  E=generatePrimeNumber(4)

# Step 5: Find D. 
#For Finding D: It must satisfies this property:-  (D*E)Mod(eulerTotient)=1;
#Now we have two Choices
# 1. That we randomly choose D and check which condition is satisfying above condition.
# 2. For Finding D we can Use Extended Euclidean Algorithm: ax+by=1 i.e., eulerTotient(x)+E(y)=GCD(eulerTotient,e)
#Here, Best approach is to go for option 2.( Extended Euclidean Algorithm.)

def gcdExtended(E,eulerTotient):
  a1,a2,b1,b2,d1,d2=1,0,0,1,eulerTotient,E

  while d2!=1:

    # k
    k=(d1//d2)

    #a
    temp=a2
    a2=a1-(a2*k)
    a1=temp

    #b
    temp=b2
    b2=b1-(b2*k)
    b1=temp

    #d
    temp=d2
    d2=d1-(d2*k)
    d1=temp

    D=b2

  if D>eulerTotient:
    D=D%eulerTotient
  elif D<0:
    D=D+eulerTotient

  return D


D=gcdExtended(E,eulerTotient)
public = (E,N)
private = (D,N)

def encryption(pub_key,n_text):
    e,n=pub_key
    x=''
    m=0
    for i in n_text:
        m=ord(i)
        c=(m**e)%n
        x+=chr(c)
    return x

'''DECRYPTION ALGORITHM'''
def decryption(priv_key,c_text):
    d,n=priv_key
    x=''
    m=0
    for i in c_text:
        m=ord(i)
        c=(m**d)%n
        x+=chr(c)
    return x

#def submit message and choose option
message_label = tk.Label(root,text='Type your content to encrypt or decrypt:',width=100,background="white").grid(row=6,column=0,columnspan=2,pady=10)
message_entry=tk.Entry(root,textvariable=message_var,width=100,background="#eee").grid(row=7,column=0,columnspan=2,pady=10)
   
choose_label = tk.Label(root,text="Type '1' for encryption and '2' for decrytion:",width=50,background="white").grid(row=8,column=0,columnspan=2,pady=10)
choose_entry=tk.Entry(root,textvariable=choose_var,width=50,background="#eee").grid(row=8,column=1,columnspan=2,pady=10)

def addToClipBoard(text):
    command = 'echo ' + text + '| clip'
    os.system(command)
     
def submit():
    #Message1
    message = message_var.get()
    #Choose Encrypt or Decrypt and Print
    choose = choose_var.get()
    if(choose==1):
        msg=tk.Label(root,bg='white')
        msg.config(text="Your encrypted message is : ")
        msg.grid(row=9,column=1)
        value=tk.Label(root)
        value.config(text=encryption(public,message))
        value.grid(row=10,column=1,padx=10,pady=10)
        encryption_btn.set("Data Encypted")
        refresh_btn=tk.Button(root,background='#2fbf71',fg='white',text="Refresh",command=lambda:refresh())
        refresh_btn.grid(row=11,column=1)
        copy_btn=tk.Button(root,background='#2fbf71',fg='white',text="Copy",command=lambda:addToClipBoard(encryption(public,message)))
        copy_btn.grid(row=11,column=2)
        def refresh():
            msg.grid_forget()
            value.grid_forget()
        print("Your encrypted message is:",encryption(public,message))
        print("Thank you for using the RSA Encryption")
    elif(choose==2):
        msg=tk.Label(root,bg='white')
        msg.config(text="Your Decrypted message is : ")
        msg.grid(row=9,column=1)
        value=tk.Label(root)
        value.config(text=decryption(private,message))
        value.grid(row=10,column=1,padx=10,pady=10)
        encryption_btn.set("Data Decrypted")
        refresh_btn=tk.Button(root,background='#2fbf71',fg='white',text="Refresh",command=lambda:refresh())
        refresh_btn.grid(row=11,column=1)
        def refresh():
            msg.grid_forget()
            value.grid_forget()
        print("Your decrypted message is:",decryption(private,message))
        print("Thank you for using the RSA Encryption")
    else:
        msg=tk.Label(root,text="        Wrong Decision!!!          ",fg='red',bg='white').grid(row=9,column=1)
        value=tk.Label(root,text=encryption(public,message),fg='white',bg='white').grid(row=10,column=1,padx=10,pady=10)

    
# open file button
open_button = tk.Button(root, width=50,background="cyan", textvariable=encrypt_btn, command=lambda:encrypt())
encrypt_btn.set("Encrypt a file")
open_button.grid(row=4,column=0)
decrypt_button = tk.Button(root, width=50,background="cyan",textvariable=decrypt_btn, command=lambda:decrypt())
decrypt_btn.set("Decrypt a file")
decrypt_button.grid(row=4,column=1)

instruction=tk.Label(root, text="Write Your Data to Encrypt/Decrypt", font="Raleway",background="#eee",width=100)
instruction.grid(row=5,column=0,columnspan=2,pady=20)

encryption_button = tk.Button(root, width=50,background="cyan", textvariable=encryption_btn, command=submit)
encryption_btn.set("Encrypt/Decrypt data")
encryption_button.grid(row=9,column=0)

root.mainloop()