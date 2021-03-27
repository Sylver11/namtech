from flask_assets import Bundle
import os


def compile_assets(assets):
    main_css_bundle = Bundle(
            'src/css/*.css',
            filters='cssmin',
            output='dist/css/main.min.css',
            extra={'rel': 'stylesheet/css'}
        )

    vendor_css_bundle = Bundle(
            'src/css/vendors/*.css',
            filters='cssmin',
            output='dist/css/vendor.min.css',
            extra={'rel': 'stylesheet/css'}
        )

    vendor_js_bundle = Bundle(
            'src/js/vendors/jquery.js',
            'src/js/vendors/bootstrap.bundle.js',
            'src/js/vendors/notify.js',
            filters='jsmin',
            output='dist/js/vendor.min.js'
        )


    assets.register('main_css', main_css_bundle)
    assets.register('vendor_js', vendor_js_bundle)
    assets.register('vendor_css', vendor_css_bundle)
    if os.getenv('FLASK_ENV') == 'DEVELOPMENT':
        main_css_bundle.build()
        main_js_bundle.build()
