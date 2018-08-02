from hashlib import sha256
import decimal
import base64


class Payeer:
    _template_string = """
    <form method="post" action="https://payeer.com/merchant/">
        <input type="hidden" name="m_shop" value="{m_shop}">
        <input type="hidden" name="m_orderid" value="{m_orderid}">
        <input type="hidden" name="m_amount" value="{m_amount}">
        <input type="hidden" name="m_curr" value="{m_curr}">
        <input type="hidden" name="m_desc" value="{m_desc}">
        <input type="hidden" name="m_sign" value="{m_sign}">
        <!--
        <input type="hidden" name="form[ps]" value="2609">
        <input type="hidden" name="form[curr[2609]]" value="USD">
        -->
        <!--
        <input type="hidden" name="m_params" value="">
        -->
        <div class="text-center">
            <input type="submit" name="m_process" value="{button_text}" class="{button_classes}"/>
        </div>
    </form>
    """
    _available_currencies = ('USD', 'EUR', 'RUB')

    def __init__(
            self,
            m_amount,
            m_curr,
            m_desc,
            m_shop,
            m_orderid,
            m_key,
            button_text,
            button_classes=False
    ):
        self._m_amount = round(decimal.Decimal(m_amount), 2)

        if m_curr not in self._available_currencies:
            raise ValueError("m_curr - может быть только одним из списка: 'USD', 'EUR', 'RUB'")
        else:
            self._m_curr = m_curr

        encoded_desc = base64.b64encode(bytes(m_desc, "utf-8"))
        self._m_desc = encoded_desc.decode("utf-8")
        self._m_shop = m_shop
        self._m_orderid = m_orderid
        self._m_key = m_key
        self._button_text = button_text
        self._button_classes = button_classes if button_classes else 'btn btn-success btn-lg'

        self._make_sign()

    def _make_sign(self):
        list_of_value_for_sign = map(
            str, [self._m_shop, self._m_orderid, self._m_amount, self._m_curr, self._m_desc, self._m_key])
        result_string = ":".join(list_of_value_for_sign)
        sign_hash = sha256(result_string.encode())
        sign = sign_hash.hexdigest().upper()
        self._sign = sign

    def get_hash(self, *args):
        list_of_value_for_sign = map(
            str, args + (self._m_key,))
        result_string = ":".join(list_of_value_for_sign)
        sign_hash = sha256(result_string.encode())
        sign = sign_hash.hexdigest().upper()
        return sign

    def get_merchant_form(self):
        return self._template_string.format(
            m_shop=self._m_shop,
            m_orderid=self._m_orderid,
            m_amount=self._m_amount,
            m_curr=self._m_curr,
            m_desc=self._m_desc,
            m_sign=self._sign,
            button_text=self._button_text,
            button_classes=self._button_classes
        )

    def print_debug_info(self):
        for k, v in self.__dict__.items():
            print(k, '-->', v)
