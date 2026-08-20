import django
from argostranslate import package

django.setup()
from django.conf import settings

package.update_package_index()

available_packages = package.get_available_packages()

translation_codes = [code for code, _ in settings.LANGUAGES if code != "en"]

package_to_install = next(
    p
    for p in available_packages
    if p.from_code == "en" and p.to_code in translation_codes
)

download_path = package_to_install.download()

package.install_from_path(download_path)
