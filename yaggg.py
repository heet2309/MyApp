# import yagmail

# server = yagmail.SMTP("heetlahute@gmail.com","myuh ajbw mlzu qlvo")


# sending = server.send("heetlahute@gmail.com","a mail","sendmail.html")

# import yagmail as mail

# import random as rand

# try:
    
#     rand_num = rand.randint(999, 10000)
    
#     smtp_server = mail.SMTP("heetlahute@gmail.com","myuh ajbw mlzu qlvo")
    
#     otp = f"{rand_num}" 
    
#     send_mail = smtp_server.send("2203031057125@paruluniversity.ac.in","otp sending",otp)  
    
#     print("done")
    

# except Exception as e:
#     print(str(e))    

import yagmail as mail
import random as rand

try:
    # Generate OTP
    rand_num = rand.randint(999, 10000)
    otp = f"{rand_num}"

    # Prepare the dynamic HTML content
    with open("otp.html", "r") as file:
        html_content = file.read()

    # Replace placeholder in HTML with the generated OTP
    dynamic_html = html_content.replace("<!-- Replace with dynamic OTP -->", f"<div class='otp'>{otp}</div>")

    # Set up SMTP server
    smtp_server = mail.SMTP("heetlahute@gmail.com", "myuh ajbw mlzu qlvo")

    # Send email with the modified HTML
    smtp_server.send(
        to="210303108276@paruluniversity.ac.in",
        subject="OTP Registration",
        contents=dynamic_html
    )

    print("Email sent successfully.")

except Exception as e:
    print(str(e))
