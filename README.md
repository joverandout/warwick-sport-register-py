# warwick-sport-register-py
Python script that reads an email, looks for forwarded booking confirmations from warwick sport and compiles a register, using flask this is then outputted to a
webpage

This python script should work such that:\
  When people book onto a warwick sports club session they simply forward their confirmation email to a gmail account, say "example@gmail.com"\
  The script scans the emails on that account, and searches for ones which it detects are warwick sport confirmation emails\
  It then checks the name and date\
  This allows the script to then comprise a register for a particular session. This will allow checking if participants of a particular session have
  booked without unnecessary hassle of checking individual email receipts
  
Index.php in the tempaltes file is a webpage that can host and run the python script and output a register so the application can be run from a phone
