$(document).ready(() => {
    function getDataUri(url) {
        var image = new Image();
        let k = ''
        image.onload = function () {
            var canvas = document.createElement('canvas');
            canvas.width = this.naturalWidth; 
            canvas.height = this.naturalHeight; 
            canvas.getContext('2d').drawImage(this, 0, 0);
            canvas.toDataURL('image/png').replace(/^data:image\/(png|jpg);base64,/, '');
            k = canvas.toDataURL('image/png');
            docDefinition.content[1].columns[0].image = k;
        };
        image.src = url;
        return k;
    }
    let preId = document.location.href;
    let id = [...preId][preId.length-1]
    $("#menuOpen").on("click", () => {
        $("#menu").toggleClass("open");
    })
    $("#menuClose").on("click", () => {
        $("#menu").toggleClass("open");
    })      
    $('.get_contact_resume').on('click', ()=>{
        axios
            .get(`${preId}/get_contact_resume`)
            .then((response)=>{
                let data = response.data
                if(data.name){
                    $('.modal_name_resume .lead').html(data.name)
                }else{
                    $('.modal_name_resume .lead').html('Нет данных')
                }
                if(data.phone){
                    $('.modal_number_resume .lead').html(data.phone)
                }else{
                    $('.modal_number_resume .lead').html('Нет данных')
                }
                if(data.email){
                    $('.modal_email_resume .lead').html(data.email)
                }else{
                    $('.modal_email_resume .lead').html('Нет данных')
                }
                console.log(data)
            })
    })
    $('.get_contact_vac').on('click', ()=>{
        axios
            .get(`${preId}/get_contact_vac`)
            .then((response)=>{
                let data = response.data
                if(data.phone){
                    $('.modal_number_vac .lead').html(data.phone)
                }else{
                    $('.modal_number_vac .lead').html('Нет данных')
                }
                if(data.email){
                    $('.modal_email_vac .lead').html(data.email)
                }else{
                    $('.modal_email_vac .lead').html('Нет данных')
                }
                console.log(data)
            })
    })
    $("#btnSearch").on("click", () => {
        let text = $("#textForSearch").val().trim().toLowerCase()
        if (text) {
            window.location.href = `?find=${text}`
        } else {
            window.location.href = `/work/resumes/`
        }
    })
    $("#vacSearch").on("click", () => {
        let text = $("#vacText").val().trim().toLowerCase()
        if (text) {
            window.location.href = `?find=${text}`
        } else {
            window.location.href = `/work/vacancies/`
        }
    })
    $('.experience').parent().before(function() {
        return '<h3> Данные для работодателя </h3>';
    });
    
    $('.specialization').parent().before(function() {
        return '<h3> Специальность </h3>';
    });
    $('.languages').parent().before(function() {
        return '<h3> Языки </h3>';
    });
    $(function () {
        $('[data-toggle="tooltip"]').tooltip({placement:'bottom'})
    });
    $('.arrows_down_arrow').on('click', function() {
    
        $('html, body').animate({
            scrollTop: $('.vacancies_container').offset().top
        }, {
            duration: 370,   // по умолчанию «400» 
            easing: "linear" // по умолчанию «swing» 
        });
    
        return false;
    });
    var docDefinition = {
        content: [
            {
                text: 'Личная информация\n',
                style: 'header'
            },
            {
                alignment: 'justify',
                columns: [
                    {
                        image: '',
                        width: 200,
                       
                    },
                    {
                        ul: [
                            `Фамилия: ${$('.res_fam').html()} \n`,
                            `Имя: ${$('.res_name').html()} \n`,
                            `Отчество: ${$('.res_patr').html()} \n`,
                            `Номер телефона: ${$('.res_num').html()} \n`,
                            `Почта: ${$('.res_mail').html()} \n`,
                        ],
                        margin: [10, 10],
                    },    
                ]
                
            },
            {
                text: 'Данные для работодателя\n\n',
                style: 'header'
            },
            {
                ul: [
                    `Опыт работы: ${$('.res_experience').val()} \n\n`,
                    `Название: ${$('.res_title').val()} \n\n`,
                ],
            },
            {
                text: 'Специальность\n\n',
                style: 'header'
            },
            {
                ul: [
                    `Специальность: ${$('.res_specialization').val()} \n\n`,
                    `Желаемая зарплата: ${$('.res_zp').val()} \n\n`,
                    `Ключевые навыки: ${$('.res_skills').val()} \n\n`,
                    `О себе: ${$('.res_about').val()} \n\n`,
                ],
            },
            {
                text: 'Языки\n\n',
                style: 'header'
            },
            {
                ul: [
                    `Родной язык: ${$('.res_native').val()} \n\n`,
                    `Иностранный язык: ${$('.res_foreign').val()} \n\n`,
                ],
            }
        ],
        styles: {
            header: {
                fontSize: 18,
                bold: true
            },
            bigger: {
                fontSize: 15,
                italics: true
            }
        } 
    };
   
    $('.save_pdf').on('click', ()=>{
        getDataUri($(".vacancies_photo").attr("src"))
        setTimeout(()=>{
            pdfMake.createPdf(docDefinition).download('resume.pdf');
        }, 100)
    })
})