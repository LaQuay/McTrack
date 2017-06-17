package dev.juanmarc.tracking.mctrackdemo

import android.os.Bundle
import android.support.v7.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if (savedInstanceState == null) {
            val ft = supportFragmentManager.beginTransaction()

            ft.setCustomAnimations(
                    R.anim.abc_fade_in, R.anim.abc_fade_out, R.anim.abc_popup_enter, R.anim.abc_popup_exit)
            ft.replace(R.id.activity_base_content, MainFragment())
            ft.addToBackStack(null)
            ft.commit()
        }
    }
}
