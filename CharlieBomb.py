import paramiko
import getpass
import subprocess
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
def get_ssh_credentials():
    # Prompt the user for the Raspberry Pi's IP address
    pi_ip = input("Enter the IP address of your Raspberry Pi: ")

    # Prompt the user for SSH credentials
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # Prompt the user for the wireless interface
    wifi_interface = input("Enter the wireless interface (e.g., wlan0): ")

    return pi_ip, username, password, wifi_interface

def connect_and_run_commands(pi_ip, username, password, wifi_interface):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the Raspberry Pi using SSH
        ssh.connect(pi_ip, username=username, password=password)
        print(f"Connected to Raspberry Pi at {pi_ip}")

        # Open a terminal and run the 'su' command
        stdin, stdout, stderr = ssh.exec_command('su')

        # Input the password provided by the user
        stdin.write(password + '\n')
        stdin.flush()

        # Run the 'airodump-ng' command with the specified wireless interface
        airodump_command = f'airodump-ng {wifi_interface}'
        stdin, stdout, stderr = ssh.exec_command(airodump_command)

        # Display the output of the 'airodump-ng' command
        print(stdout.read().decode())

        # Close the SSH connection
        ssh.close()
    except paramiko.AuthenticationException:
        print("Authentication failed. Make sure you have the correct credentials.")
    except paramiko.SSHException as e:
        print(f"SSH error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Always close the SSH connection, if it's open
        if ssh.get_transport() is not None:
            ssh.close()

if __name__ == "__main__":
    pi_ip, username, password, wifi_interface = get_ssh_credentials()
    connect_and_run_commands(pi_ip, username, password, wifi_interface)
