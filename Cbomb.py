import os

banner = '''

                               ________________
                          ____/ (  (    )   )  \___
                         /( (  (  )   _    ))  )   )\
                       ((     (   )(    )  )   (   )  )
                     ((/  ( _(   )   (   _) ) (  () )  )
                    ( (  ( (_)   ((    (   )  .((_ ) .  )_
                   ( (  )    (      (  )    )   ) . ) (   )
                  (  (   (  (   ) (  _  ( _) ).  ) . ) ) ( )
                  ( (  (   ) (  )   (  ))     ) _)(   )  )  )
                 ( (  ( \ ) (    (_  ( ) ( )  )   ) )  )) ( )
                  (  (   (  (   (_ ( ) ( _    )  ) (  )  )   )
                 ( (  ( (  (  )     (_  )  ) )  _)   ) _( ( )
                  ((  (   )(    (     _    )   _) _(_ (  (_ )
                   (_((__(_(__(( ( ( |  ) ) ) )_))__))_)___)
                   ((__)        \\||lll|l||///          \_))
                            (   /(/ (  )  ) )\   )
                          (    ( ( ( | | ) ) )\   )
                           (   /(| / ( )) ) ) )) )
                         (     ( ((((_(|)_)))))     )
                          (      ||\(|(|)|/||     )
                        (        |(||(||)||||        )
                          (     //|/l|||)|\\ \     )
                        (/ / //  /|//||||\\  \ \  \ _)
-------------------------------------------------------------------------------
                                 CH4RL13 B0MB
                           "Like a warm slice of PI"
'''
print(banner)

def connect_locally(interface, filename):
    password = input("Enter your 'su' password: ")
    os.system(f"su -c 'airodump-ng -w {filename} {interface}'")

def connect_remotely(ip, interface, username, password, filename):
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, username=username, password=password)
        channel = ssh.invoke_shell()

        # Run 'su' command and enter the password
        channel.send("su\n")
        channel.recv(1000)  # Wait for the password prompt
        channel.send(password)

        # Run 'airodump-ng' command
        command = f"airodump-ng -w {filename} {interface}\n"
        channel.send(command)

        # Wait for the command to finish
        while True:
            output = channel.recv(1024).decode()
            if "airodump-ng: quitting" in output:
                break

    except Exception as e:
        print(f"SSH Connection Failed: {str(e)}")
    finally:
        ssh.close()

def main():
    local_or_remote = input("Are we local? (yes/no): ").strip().lower()

    if local_or_remote == "yes":
        interface = input("Enter wireless interface: ")
        filename = input("Enter desired file name: ")
        connect_locally(interface, filename)
    elif local_or_remote == "no":
        ip = input("Enter Raspberry Pi IP: ")
        username = input("Enter your username: ")
        password = input("Enter your 'su' password: ")
        interface = input("Enter desired wireless interface: ")
        filename = input("Enter desired file name: ")
        connect_remotely(ip, interface, username, password, filename)
    else:
        print("Invalid input. Please enter 'yes' or 'no.")

if __name__ == "__main__":
    main()
