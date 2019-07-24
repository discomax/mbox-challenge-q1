
import mailbox as mb
from email import utils, message

# Store the file path associated with the file (note the backslash may be OS specific)
file = 'mbox.full'
mbox = mb.mbox(file)
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
            div = ""
            print(div)
            #print(sub_msg.__dict__)
            #print(sub_msg.get_content_type())
            #print(subMsg)
            #lines = subMsg.splitlines(_m
            #print(vars(sub_msg))
            reverse_payload(sub_msg)
            div = '------------------------'
    else:
    # create new message with reversed 
        #print(mbox_msg.__dict__)
        #orig_content = mbox_msg.get_payload()
        print(payload)
        print(type(payload))
        lines = payload.splitlines()
        rev_lines = lines[::-1]
        print(type(rev_lines))
        #print(orig_content)
        print(rev_lines)
        rev_payload = "\n".join(rev_lines)
        print(rev_payload)


def revise_msg(mbox_msg):
    # takes an Mbox mail meassage as the argument
    # creates a new Mbox meassage instance with the lines 
    # of the message body/payload in reverse order.
    # returns the new Mbox message.
    msg = mbox_msg
    payload = mbox_msg.get_payload()
    reverse_payload(msg)
    
    
#for message in mbox:
revise_msg(mbox[10])
mbox.unlock()
#if __name__ == '__main__':
    
#print(repr(msg_body))
