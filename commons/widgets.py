import json
from django.utils.safestring import mark_safe
from django.forms import DateInput, TimeInput, SelectMultiple
from .library import get_index_value
from .constants import WIDGET_DATE_FORMAT, DATE_i18n, WIDGET_TIME_FORMAT


class DatePickerInput(DateInput):
    def render(self, name, value, attrs=None, renderer=None):
        unsafe_html = super(DatePickerInput, self)\
            .render(name, value, attrs=attrs, renderer=None)
        options = json.dumps({
            'format': WIDGET_DATE_FORMAT,
            'i18n': DATE_i18n,
            'autoClose': True
        })
        js = '''<script type="text/javascript">
        <!--//
            window.addEventListener('DOMContentLoaded', function (event)  {
                 M.Datepicker.init(
                    document.getElementById("%(date_id)s"), %(options)s
                );
            });
        //-->
        </script>
        ''' % {'date_id': attrs['id'], 'options': options}
        return mark_safe(unsafe_html + js)


class TimePickerInput(TimeInput):
    def render(self, name, value, attrs=None, renderer=None):
        unsafe_html = super(TimePickerInput, self)\
            .render(name, value, attrs=attrs, renderer=None)
        options = json.dumps({
            'format': WIDGET_TIME_FORMAT,
            'i18n': DATE_i18n,
            'twelveHour': False,
            'autoClose': True
        })

        js = '''<script type="text/javascript">
        <!--//
            window.addEventListener('DOMContentLoaded', function (event)  {
                M.Timepicker.init(
                    document.getElementById("%(date_id)s"), %(options)s
                );
                $("#%(date_id)s").on('change', function() {
                    let receivedVal = $(this).val();
                    $(this).val(receivedVal + ":00");
                });
            });
        //-->
        </script>
        ''' % {'date_id': attrs['id'], 'options': options}
        return mark_safe(unsafe_html + js)


class SelectMultiplePickerInput(SelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        unsafe_html = super(SelectMultiplePickerInput, self)\
            .render(name, value, attrs=attrs, renderer=None)

        options = json.dumps({})
        values = ','.join(
            *[map(lambda elem: get_index_value(elem), value)]) if value else ''
        js = '''<script type="text/javascript">
        <!--//
            window.addEventListener('DOMContentLoaded', function (event)  {
                var elems = document.querySelectorAll('select');
                M.FormSelect.init(elems,  %(options)s);
                options = Array.from(document.querySelectorAll('#%(date_id)s option'));
                var values = '%(values)s';
                values.split(',').forEach(function(v) {
                  options.find(c => c.value == v).selected = true;
                });
                M.FormSelect.init(elems,  %(options)s);
            });

        //-->
        </script>
        ''' % {'date_id': attrs['id'], 'options': options, 'values': values}
        return mark_safe(unsafe_html + js)
