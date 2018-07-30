$(document).ready(function () {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        var host = document.location.host;
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // -------------------------------- Верификация пользователя - верифицировать --------------------------------

    $('#verify_v_user').click(function (e) {
        e.preventDefault();

        $.ajax({
            url: window.location.href,
            data: {
                action: 'verify_user'
            },
            method: 'post',
            success: function (response) {
                if (response.status) {
                    window.location.reload();
                }
            },
            error: function () {
                console.log('Error');
            }
        });

    });

    // -------------------------------- Верификация пользователя - запрос кодов на верификацию --------------------------------

    var counter_get_codes = 0;
    var counter_check_codes = 0;
    var get_codes_btn = $('#get_codes');
    var check_codes_btn = $('#check_codes');
    get_codes_btn.click(function (e) {
        if (counter_get_codes == 0) {
            $.ajax({
                url: window.location.href,
                data: {
                    action: 'need_codes'
                },
                method: 'post',
                success: function(response) {
                    if (response.status) {
                        get_codes_btn.hide();
                        check_codes_btn.show();
                    }
                },
                error: function() {
                    console.log('Error');
                },
            });
        }
        counter_get_codes++;
    });

    // -------------------------------- Верификация пользователя - проверка кодов --------------------------------

    check_codes_btn.click(function () {
        if (counter_check_codes == 0) {
            if ($('#email_code').val().length != 5 && $('#phone_code').val().length != 5) {
                alert('Коды должны содержать 5 цифр');
            } else {
                check_codes_btn.hide();
                $.ajax({
                    url: window.location.href,
                    data: {
                        action: 'check_codes',
                        email_code: $('#email_code').val(),
                        phone_code: $('#phone_code').val()
                    },
                    method: 'post',
                    success: function (response) {
                        if (response.status) {
                            window.location.reload();
                        } else {
                            alert(response.message);
                        }
                    },
                    error: function () {
                        console.log('Error');
                    },
                });
                counter_check_codes++;
            }
        }
    });

    $('#save_needed_document').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: window.location.href,
            data: {
                action: 'check_documents',
            },
            method: 'post',
            success: function (response) {
                if (response.status) {
                    window.location.reload();
                } else {
                    alert(response.message);
                }
            },
            error: function () {
                console.log('Error');
            },
        });
    });

    $('#need_documents').click(function (e) {
        e.preventDefault();
        var message_for_user = prompt('Укажите, каки именно документов не хватает');

        $.ajax({
            url: window.location.href,
            data: {
                action: 'need_documents',
                message: message_for_user
            },
            method: 'post',
            success: function (response) {
                if (response.status) {
                    window.location.href = response.redirect_url;
                } else {
                    alert(response.message);
                }
            },
            error: function () {
                console.log('Error');
            },
        });

    });

    $('#refuse').click(function (e) {
        e.preventDefault();

        $.ajax({
            url: window.location.href,
            data: {
                action: 'refuse'
            },
            method: 'post',
            success: function (response) {
                if (response.status) {
                    window.location.href = response.redirect_url;
                } else {
                    alert(response.message);
                }
            },
            error: function () {
                console.log('Error');
            },
        });

    });

    // -------------------------------- Финансы - перевод личных средств --------------------------------

    var sendMoneyRecipient = $('.send-money #id_recipient');
    var recipientFullname = $('#recipient_fullname');
    var submitBtn = $('.send-money #submit-btn');
    
    sendMoneyRecipient.on('input', function () {
        var recipient = $(this).val();
        var patt = new RegExp("CT-[0-9][0-9][0-9][0-9][0-9][0-9][0-9]");
        var isTrue = patt.test(recipient);

        if (isTrue && (recipient.length === 10)) {
            $.ajax({
                url: window.location.href,
                data: {
                    recipient_js: recipient
                },
                method: 'post',
                success: function (response) {
                    if (response.status) {
                        recipientFullname.text(response.recipient);
                        recipientFullname.parent('.alert').show();
                        submitBtn.removeAttr('disabled');
                    } else {
                        recipientFullname.text('');
                        recipientFullname.parent('.alert').hide();
                        submitBtn.attr('disabled', 'disabled');
                    }
                },
                error: function () {
                    console.log('Error')
                }
            });
        } else {
            recipientFullname.parent('.alert').hide();
            submitBtn.attr('disabled', 'disabled');
        }
    });

    // -------------------------------- Смена направления регистрации --------------------------------
    $('.change-direction-link').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('data-path'),
            method: 'POST',
            data: {
                action: $(this).attr('data-action')
            },
            success: function (response) {
                if (response.status) {
                    window.location.reload()
                }
            },
            error: function () {
                console.log('Error')
            }
        });
    })

});