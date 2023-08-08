// // // // // // // // // // // // // // // // 
// CONFIGURING DROPAREA (the form textarea)  // 
// // // // // // // // // // // // // // // // 
const droparea = document.getElementsByTagName("textarea")[0];

droparea.addEventListener("dragover", (e) => {
    e.preventDefault();
    droparea.classList.add("hover");
});

droparea.addEventListener("dragleave", () => {
    droparea.classList.remove("hover");
});

droparea.addEventListener("drop", (e) => {
    // two statements to prevent the default behaviour
    e.preventDefault();
    e.stopImmediatePropagation();
    // changing back format to normal
    droparea.classList.remove("hover");

    // only going to get the first file (support for upload 1 by 1)
    const image = e.dataTransfer.files[0];
    const type = image.type;

    // support only images
    if (
        type == "image/png" ||
        type == "image/jpg" ||
        type == "image/jpeg"
    ) {
        return upload(image);
    } else {
        alert("Invalid File Format!");
        return false;
    }

});

const upload = (file) => {
    console.log("upload being executed")
    const fileInput = document.querySelector("input[type='file']");
    // const form = document.forms[2];
    const form = document.getElementById('file-form');



    // Create a new FileList with the given file
    const fileList = new DataTransfer();
    fileList.items.add(file);

    // Fill the input element
    fileInput.files = fileList.files;

    // Submit the form
    form.submit()
};

// // // // // // // // // // // // // // // // // // // // 
// MAKING THE FILE FORM INVISIBLE                        // 
// // // // // // // // // // // // // // // // // // // // 

// I use one of the Bootstrap classes for this: "d-none"
const allFormDivs = document.querySelectorAll("div[class='form-group']");
const hiddenForm = allFormDivs[2]
hiddenForm.classList.add("d-none");

// // // // // // // // // // // // // // // // // // // // 
// ADDING FILES UPLOADED (READY TO SUBMIT WITH COMMENT)  // 
// // // // // // // // // // // // // // // // // // // // 

function addFilesReadyToSubmit() {

    // const parentElement = document.querySelectorAll('.form-group')[0];
    const parentElement = document.getElementById('form-group-comment');
    const addCommentButton = document.getElementById('button-submit-comment');
    // const addCommentButton = document.querySelectorAll('button[type="submit"]')[0];


    addCommentButton.classList.add("mt-2") // crispy forms setup needs a bit more of margin here

    const attachments = JSON.parse(document.getElementById("new_comment_attachments").textContent);
    for (let i = 0; i < attachments.length; i++) {
        console.log(attachments[i]);
        console.log(attachments[i].name);
        console.log(attachments[i].url);

        const newElement = document.createElement("div");
        const newButton = document.createElement("button");
        newButton.textContent = attachments[i].name;
        newButton.setAttribute("onclick", "location.href='" + attachments[i].url + "'");
        newButton.classList.add('btn');
        newButton.classList.add('btn-link');
        newButton.classList.add('btn-sm');
        newButton.classList.add('p-1');
        newButton.classList.add('my-1');
        newElement.appendChild(newButton)
        parentElement.insertBefore(newElement, addCommentButton);
    }
}
addFilesReadyToSubmit();
