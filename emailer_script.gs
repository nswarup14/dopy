function listFolderContents() {
  prefix_str_email = 'f20';
  prefix_str_email_m = 'h20';
  prefix_str_email_p = 'p20';
  suffix_str_email = '@pilani.bits-pilani.ac.in';
  
  var foldername = 'Photobooth.';
  var folderlisting = 'listing of folder ' + foldername;
  
  var folders = DriveApp.getFoldersByName(foldername)
  var folder = folders.next();
  var contents = folder.getFolders();
  
  var ss = SpreadsheetApp.create(folderlisting);
  var sheet = ss.getActiveSheet();
  sheet.appendRow( ['name', 'link', 'email'] );
  
  var file;
  var name;
  var link;
  var row;
  var email;
  while(contents.hasNext()) {
    file = contents.next();
    name = file.getName();
    link = file.getUrl();
    
    // Adding prefix
    if (name[0] == 'M') {
      email = prefix_str_email_m;
    }
    else if (name[0] == 'P') {
      email = prefix_str_email_p;
    }
    else {
      email = prefix_str_email;
    }
    
    // Suffix for M and P
    if (name[0] == 'P' || name[0] == 'M') {
      if (name[2] != '7' && name[2] != '8') {
        email += name.substring(1,3) + name.substring(4,7) + suffix_str_email;
      } // M160046
      else {
        email += name.substring(1,7) + suffix_str_email;
      } // M180045
    }
    // Suffix for first degrees
    else {    
      if (name[1] != '7' && name[1] != '8') {
        email += name.substring(0,2) + name.substring(3,6) + suffix_str_email;
      }
      else {
        email += name.substring(0,6) + suffix_str_email;
      }
    }
    
    sheet.appendRow([name, link, email]);
  }  
};
