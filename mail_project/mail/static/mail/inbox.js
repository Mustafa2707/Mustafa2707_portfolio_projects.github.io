document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#form_submit').addEventListener('click', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


function toTitleCase(str) {
  return str.replace(
    /\w\S*/g,
    text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
  );
}

function recipientDetails(){
  var popup = document.getElementById("myPopup");
  popup.classList.toggle("show");
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-details').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';


}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-details').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Display appropriate mailbox
  fetch(`/emails/${mailbox}`,{
    method:"GET"
  })
  .then(responce => responce.json())
  .then(emails  => {

      emails.forEach(email => {
        let sender = email.sender;
        let recipients = email.recipients;
        let subject = email.subject;
        let timestamp = email.timestamp;

        const new_email = document.createElement('div');
        new_email.style.border = '1px solid grey';
        new_email.style.borderRadius= '5px';
        new_email.style.padding = '2%';
        new_email.style.marginBottom = '2%';

        new_email.innerHTML = `
        <div><h4>${subject.toUpperCase()}</h4></div>
        <div>Sent By: ${sender}</div>
        <div>${recipients}</div>
        <div>${timestamp}</div>

        `;

        new_email.addEventListener('click',()=> getEmail(email.id,mailbox));

        if (email.read) {
          new_email.style.backgroundColor = '#D3D3D3';
          new_email.style.color='white';
      }else{
          new_email.style.backgroundColor = '#FFFFFF';
      }

        console.log(email);
        document.querySelector('#emails-view').appendChild(new_email);
      });
  })
  
}

function send_email(){
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(responce => responce.json())
  .them(email =>{
    console.log(email)
  })
  .then(result => {
    console.log(result)
  })

  load_mailbox('sent')
}

function archive_email(email_id){

  fetch(`/emails/${email_id}`,{
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })

  load_mailbox('inbox');
}

function unarchive(email_id){
  fetch(`/emails/${email_id}`,{
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })

  load_mailbox('inbox');
}

function email_read(email_id){
  fetch(`/emails/${email_id}`,{
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}
function email_mark_unread(email_id){
  fetch(`/emails/${email_id}`,{
    method: 'PUT',
    body: JSON.stringify({
      read: false
    })
  })
}

function reply_to_email(email_id){
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-details').style.display = 'none';

 // fetch email
 fetch(`/emails/${email_id}`, {
   method: 'GET'
 })
 .then(responce => responce.json())
 .then(email => {
   let recipient = email.sender;
   let subject = '';
   if (email.subject.slice(0, 3) === "Re: "){
     subject = email.subject;
   }
   else{
     subject = `Re: ${email.subject}`;
   }

   let body = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;

   document.querySelector('#compose-recipients').value = recipient;
   document.querySelector('#compose-subject').value = subject;
   document.querySelector('#compose-body').value = body;
 })
}

function getEmail(email_id,mailbox){

  // Display Email page
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-details').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  


  // Fetch Email
  fetch(`/emails/${email_id}`, {
    method: 'GET'
  })
  .then(responce => responce.json())
  .then(email => {

      if (mailbox === 'inbox'){
        email_read(email_id);
        document.querySelector('#archive_button').addEventListener('click', ()=> archive_email(email_id));
      }else if (mailbox === 'archive'){
        document.querySelector('#archive_button').addEventListener('click', ()=> unarchive(email_id));
      }
      console.log(email);
      let sender = email.sender;
      let subject = email.subject;
      let recipients = email.recipients;
      let timestamp = email.timestamp;
      let body = email.body;

      

      document.querySelector('#email-subject').innerHTML = `${toTitleCase(subject)}`;
      document.querySelector('#sender-div').innerHTML = `${sender}`;
      document.querySelector('#timestamp-div').innerHTML = `${timestamp}`;
      document.querySelector('#body-div').innerHTML = `${body}`;

      document.querySelector('#p_subject').innerHTML = `${toTitleCase(subject)}`;
      document.querySelector('.p_sender').innerHTML = `${sender}`;
      document.querySelector('#p_recipients').innerHTML = `${recipients}`;
      document.querySelector('#p_date').innerHTML = `${timestamp}`;

      
      document.querySelector('#reply_button').addEventListener('click', ()=> reply_to_email(email_id));
     })
}
