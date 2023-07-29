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
    const form = document.forms[2];

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
    const parentElement = document.querySelectorAll('.form-group')[0];
    const addCommentButton = document.querySelectorAll('button[type="submit"]')[0];
    // const addCommentButton = buttons[0]
    // console.log(buttons)
    // console.log(addCommentButton)


    const newElement = document.createElement("p");
    newElement.textContent = "This is the new content";
    // const addCommentButton = document.querySelector('button:contains("Add comment")');
    parentElement.insertBefore(newElement, addCommentButton);
}
