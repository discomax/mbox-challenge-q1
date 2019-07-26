
import mailbox as mb
from email import message, charset, policy

# Store the file path associated with the file (note the backslash may be OS specific)
imput_file = 'data/mbox.full'
mbox = mb.mbox(imput_file)
mbox.lock()

"""def reverse_lines(string):
    # 
    lines = string.splitlines()
    #print(lines)
    rev_lines = lines[::-1]
    #print(rev_lines)
    return rev_lines"""
    
def reverse_payload(mail_message):
    payload = mail_message.get_payload()
    if mail_message.is_multipart():
    
        #print(mbox_msg.__dict__)
        for sub_msg in payload:              
            #div = ""
            #print(div)
            #print(type(sub_msg))
            #print(sub_msg.__dict__)
            #print(sub_msg.get_content_type())
            #print(subMsg)
            #lines = subMsg.splitlines(_m
            #print(vars(sub_msg))
            reverse_payload(sub_msg)
            #div = '------------------------'
    else:
    # create new message with reversed 
        print(mail_message.__dict__)
        #orig_content = mbox_msg.get_payload()
        print(payload)
        #print(type(payload))
        lines = payload.splitlines()
        rev_lines = lines[::-1]
        rev_payload = "\n".join(rev_lines)
        print(rev_payload)
        return rev_payload


def revise_msg(mbox_msg):
    # takes an Mbox mail meassage as the argument
    # creates a new Mbox meassage instance with the lines 
    # of the message body/payload in reverse order.
    # returns the new Mbox message.
    msg = mbox_msg
    msg_content = reverse_payload(msg)
    utf8msg = msg_content.encode("utf-8")
    print(utf8msg)
    #print(msg_content)
    msg.set_payload(msg_content)
    return msg
    #reverse_payload(msg)
    
out_file = 'data/revised_mbox.full'

#for message in mbox:

try:
    revised_mbox = mb.mbox(out_file)
    #for message in mbox:
    message = mbox[9]
    #print(message.get_payload())
    #print('\n\n')
    new_msg = revise_msg(message)
    #print(vars(new_msg))
    #revised_mbox.add(new_msg)
    #print('success')
finally:
    mbox.unlock()
    revised_mbox.clear()
    mbox.close()
#if __name__ == '__main__':
    
#print(repr(msg_body))
