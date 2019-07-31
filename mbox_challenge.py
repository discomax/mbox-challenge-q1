
import mailbox as mb
from email import message

# Store the file path associated with the file (backslash may be OS specific)
#imput_file = 'data/mbox.full'
#mbox = mb.mbox(imput_file)
#mbox.lock()

def pop_signature(line_list, delim='-- '):
    '''If present, split the signature from the lines.

    Keyword argumants:
    line_list --  a list of strings from email's payload.
    delim -- str which marks start of email signature.(default '-- ')
    '''
    if delim in line_list:
        new_list = line_list[:line_list.index(delim)]
        sig_list = line_list[line_list.index(delim):]

        return new_list, sig_list
    else:
        sig_list = []

        return line_list, sig_list


def reverse_payload(mail_message):
    msg = mail_message
    payload = msg.get_payload()
    
    lines, signature = pop_signature(payload.splitlines())
    reversed_lines = lines[::-1]
    reversed_lines.extend(signature)
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



def process_multipart(msg, payload=[]):
    """
    Reverse lines of multipart payload's string part.

    Keyword arguments:
    msg -- a multipart email Message object
    payload -- list of messages (default [])
    """
    content = msg.get_payload()
    new_payload = []
    sub_msg = content[0]
    sub_msg.set_payload(reverse_payload(sub_msg))
    msg.set_payload(new_payload)
    msg.attach(sub_msg)
    
    return msg



def revise_msg(mail_message):
    # takes an Mbox mail meassage as the argument
    # creates a new Mbox meassage instance with the lines 
    # of the message body/payload in reverse order.
    # returns the new Mbox message.
    msg = mail_message
    if msg.is_multipart():
        msg = process_multipart(msg)
    else:
        msg_content = reverse_payload(msg)    
        msg.set_payload(msg_content)
    return msg



def mbox_challenge(in_file, out_file):
    with open(in_file):
        try:
            mbox = mb.mbox(in_file)
            mbox.lock()
            revised_mbox = mb.mbox(out_file)
            for Message in mbox:
                #Message = mbox[4]
                NewMessage = revise_msg(Message)
                revised_mbox.add(NewMessage)
        except (mb.NoSuchMailboxError, mb.FormatError) as e:
            print('Error Occurerd: ', e)
        finally:
            revised_mbox.close()
            mbox.unlock()



if __name__ == "__main__":
    mbox_in = 'date/mbox.full'
    mbox_out = 'data/revised_mbox.full'
    mbox_challenge(mbox_in, mbox_out)
