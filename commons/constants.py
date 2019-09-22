
'''
variable for text when there is an empty field error
'''
EMPTY_FIELD_ERROR_TEXT = 'This field may not be blank.'

EMPTY_FIELD_REQUIRED_TEXT = 'This field is required.'
EMPTY_FIELD_REQUIRED_TEXT_ES = 'Este campo es requerido.'


'''
    variable with 210 characters
'''
TEXT_WITH_210_CHARACTERS = "01234567890123456789012345678901234567890123456789\
    01234567890123456789012345678901234567890123456789012345678901234567890123\
    45678901234567890123456789012345678901234567890123456789012345678901234567\
    890123456789"


def get_maximum_error_text_in_field(maximum_number):
    '''
        function for text when there is an maximum field error
    '''
    return 'Ensure this field has no more than {} characters.'.format(
        str(maximum_number)
    )


DATE_i18n = {
    'months': [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
        "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ],
    'monthsShort': [
        "Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Set", "Oct",
        "Nov", "Dic"
    ],
    'weekdays': [
        "Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes",
        "Sábado"
    ],
    'weekdaysShort': [
        "Dom", "Lun", "Mar", "Mie", "Jue", "Vie", "Sab"
    ],
    'weekdaysAbbrev': [
        "D", "L", "M", "M", "J", "V", "S"
    ],
    'cancel': 'Cancelar',
    'clear': 'Limpar',
    'done': 'Ok'
}


WIDGET_DATE_FORMAT = 'dd/mm/yyyy'
WIDGET_TIME_FORMAT = 'hh:mm:ss'
