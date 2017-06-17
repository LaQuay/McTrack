package dev.juanmarc.tracking.mctrackdemo

import android.os.Bundle
import android.support.v4.app.Fragment
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.github.kittinunf.fuel.Fuel

/**
 * Created by LaQuay on 17/06/2017.
 */

class MainFragment : Fragment() {
    var TAG: String = "MainFragment" //TODO Do with TAGNAME

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_main, container, false)

        testHTTP()

        return view
    }

    fun testHTTP() {
        Fuel.get("http://httpbin.org/get").responseString { request, response, result ->
            result.fold({ d ->
                //do something with data
                Log.e(TAG, d)

            }, { err ->
                //do something with error
                Log.e(TAG, err.toString())
            })
        }
    }
}