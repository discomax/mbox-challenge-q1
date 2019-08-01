'''
##Mbox Challenge

This script reads an email mbox file filled with singlepart
and multipart/mixed email messages with a content  type of 
text/plain. It takes the mbox file and genrates anoutner mbox
file with all the mbox files in the same order, but with the
lines of each individual message bady printed in reverse order.

This tool accepts text (.txt) files as well as mabox (.full) files. 

This script requires `mailbox` be installed within the  Python
environment you are running the script in.
'''

import mailbox as mb
from email import message


def pop_signature(lines, delim='-- '):
    '''Splits content into body and signature

    Args:
        lines (list) --  a list of strings from email's payload.
        delim (str) -- start of email's signature. (default '-- ')

    Returns:
        new_lines (list) -- strings of the message body.
        sig_list (list) -- strings of the message signature.
    '''
    new_lines = lines
    sig_list = []
    if delim in lines:
        new_lines = lines[:lines.index(delim)]
        sig_list = lines[lines.index(delim):]
    return new_lines, sig_list


def reverse_payload(msg):
    '''
    Returns a singlepart email's content in reversed order.

    This will take the individual lines of a message's 
    content string (payload) and reorder them last to first. 
    Any signature will remain at the end of the reordered string.

    Args:
        msg (email.Message) -- a singlepart email Message.

    Returns:
        reversed_payload(str) -- message content in reverse order.
    '''
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
    '''
    Reverse the messages singlepart content in the payload.

    Assuming the msg argument is a multipart/mixed message
    containing only a singlepart message in it's payload,
    this will reverse the payload of that singlepart message
    and reinsert it in the multipart/mixed message's payload.
    
    Args:
        msg (email.Message): a multipart email Message object
        payload (list): list of messages (default [])

    Returns: 
        msg (email.Message): object with the payload reversed per the discription

    TODO: add recursion to process other types of multipart
    messages.
    '''
    content = msg.get_payload()
    sub_msg = content[0]
    sub_msg.set_payload(reverse_payload(sub_msg))
    msg.set_payload(payload)
    msg.attach(sub_msg)
    return msg


def mbox_challenge(infile, outfile):
    '''
    Format emails from mbox file, write to new mbox file

    Take each email message in a in an mbox formated mailbox and
    reverse the order of the lines of text in the message body
    from last to first. Create a new mbox formatted mailbox and
    save it to a new file.

    Args:
        infile (.full): file containing email mailbox
        outfile (.full): new file for saving mailbox w/ formatted messages

    Raises:
        Error: problem reading, formatting or writing the mbox
    '''
    try:
        mbox = mb.mbox(infile)
        mbox.lock()
        revised_mbox = mb.mbox(outfile)
        for Message in mbox:
            if Message.is_multipart():
                NewMessage = process_multipart(Message)
                revised_mbox.add(NewMessage)
            else:
                msg_content = reverse_payload(Message)    
                Message.set_payload(msg_content)
                revised_mbox.add(Message)
    except mb.Error:
        print('An error occurred. Please check the file contents')
    finally:
        revised_mbox.close()
        mbox.unlock()


if __name__ == "__main__":
    filename= 'data/mbox.full'
    new_filename = 'data/revised_mbox.full'
    try:
        with open(filename):
            mbox_challenge(filename, new_filename)
    except IOError as e:
        print(e)
