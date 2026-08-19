from argostranslate import package

package.update_package_index()

available_packages = package.get_available_packages()

package_to_install = next(
    p for p in available_packages if p.from_code == "en" and p.to_code == "fr"
)

download_path = package_to_install.download()

package.install_from_path(download_path)

print("Modèle installé.")
