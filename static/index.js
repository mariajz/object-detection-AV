
window.onload = () => {
    $('#sendurlbutton').click(() => {
        console.log("Button clicked")
        urlval = $('#urlinput').val()
        urlbox = $('#urlimagebox')
        $.ajax({
            url: "http://localhost:5000/testurl",
            type: "POST",
            data: urlval,
            cache: false,
            processData: false,
            contentType: false,
            error: function (data) {
                console.log("upload error", data);
                console.log(data.getAllResponseHeaders());
            },
            success: function (data) {
                console.log("Success")
                bytestring = data['status']
                image = bytestring.split('\'')[1]
                urlbox.attr('src', 'data:image/jpeg;base64,' + image)
            }
        });
    });

    $('#sendbutton').click(() => {
        console.log("Image Button clicked")
        imagebox = $('#imagebox')
        input = $('#imageinput')[0]
        if (input.files && input.files[0]) {
            let formData = new FormData();
            formData.append('image', input.files[0]);
            $.ajax({
                url: "http://localhost:5000/testimage",
                type: "POST",
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                error: function (data) {
                    console.log("upload error", data);
                    console.log(data.getAllResponseHeaders());
                },
                success: function (data) {
                    bytestring = data['status']
                    image = bytestring.split('\'')[1]
                    imagebox.attr('src', 'data:image/jpeg;base64,' + image)
                }
            });
        }
    });
};

function readUrl(input) {
    imagebox = $('#imagebox')
    console.log("evoked readUrl")
    if (input.files && input.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {

            imagebox.attr('src', e.target.result);
            imagebox.height(300);
            imagebox.width(300);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

