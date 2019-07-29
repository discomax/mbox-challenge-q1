
import mailbox as mb
from email import message, charset, policy

# Store the file path associated with the file (note the backslash may be OS specific)
imput_file = 'data/mbox.full'
mbox = mb.mbox(imput_file)
mbox.lock()



def reverse_payload(mail_message):
    msg = mail_message
    payload = msg.get_payload()
    
    lines = payload.splitlines()
    reversed_lines = lines[::-1]
    reversed_payload = "\n".join(reversed_lines)
    content_type = msg.get('Content-Type')
    encoding = msg.get('Content-Transfer-Encoding')
    if 'Content-Transfer-Encoding' in msg:
        if '8bit' in encoding.lower():
            reversed_payload = reversed_payload.encode("utf-8")
        else:
            # TODO: handle other encodings (i.e. base64, Binary, x-token)
            pass
    return reversed_payload


def process_multipart(mail_message):
    msg = mail_message
    payload = msg.get_payload()
    print(len(payload))
    new_payload = []
    print(type(payload))
    '''for sub_msg in payload:
        if sub_msg.is_multipart():
            process_multipart(sub_msg)
        else:
            content = reverse_payload(msg)    
            print(content)
            msg.set_payload(content)

        if 'related' in msg.get('Content-Type').lower():
            sub_msg = sub_msg.make_related()
        elif 'alternative' in msg.get('Content-Type').lower():
            sub_msg = sub_msg.make_alternative()
        else:
            #sub_msg = sub_msg.make_mixed()
            sub_msg = '''
    sub_msg = payload[0]
    sub_msg.set_payload(reverse_payload(sub_msg))
    msg.set_payload(new_payload)
    msg.attach(sub_msg)
    print(vars(msg))
    print(len(msg.get_payload()))
    return msg

            
def revise_msg(mail_message):
    # takes an Mbox mail meassage as the argument
    # creates a new Mbox meassage instance with the lines 
    # of the message body/payload in reverse order.
    # returns the new Mbox message.
    msg = mail_message
    
    
    if msg.is_multipart():
        msg = process_multipart(msg)
        pass
    else:
        msg_content = reverse_payload(msg)    
        print(msg_content)
        msg.set_payload(msg_content)
    return msg
    #reverse_payload(msg)
    

try:
    out_file = 'data/revised_mbox.full'
    revised_mbox = mb.mbox(out_file)
    for Message in mbox:
        #Message = mbox[10]
        NewMessage = revise_msg(Message)
        #print(vars(new_msg))
        revised_mbox.add(NewMessage)
        #print('success')
finally:
    mbox.unlock()
    #revised_mbox.clear()
    mbox.close()
#if __name__ == '__main__':
    
#print(repr(msg_body))
