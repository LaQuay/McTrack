package dev.juanmarc.tracking.mctrackdemo

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.os.Handler
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
    private val TIME_FOR_NEW_AD: Long = 5000
    private val STOP_VIDEO_MILIS: Long = 10000
    private val BLACK_SCREEN_YOUTUBE: String = "https://www.youtube.com/watch?v=XIMLoLxmTDw"
    private var lastURL: String = ""

    private var handler: Handler = Handler()
    private lateinit var runnableNewUrlBackground: Runnable
    private lateinit var runnableStopVideo: Runnable

    init {
        runnableNewUrlBackground = Runnable {
            testHTTP()
            handler.postDelayed(runnableNewUrlBackground, TIME_FOR_NEW_AD)
        }

        runnableStopVideo = Runnable {
            startYoutubeIntent(BLACK_SCREEN_YOUTUBE)
        }
    }

    override fun onResume() {
        super.onResume()
        lastURL = ""
    }

    override fun onStop() {
        super.onStop()
        handler.removeCallbacks(runnableNewUrlBackground)
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_main, container, false)

        getWebsiteUrl()

        return view
    }

    fun getWebsiteUrl() {
        handler.post(runnableNewUrlBackground)
    }

    fun startYoutubeIntent(url: String) {
        handler.postDelayed(runnableStopVideo, STOP_VIDEO_MILIS)
        startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
    }

    private fun testHTTP() {
        Fuel.get("http://httpbin.org/get").responseString { request, response, result ->
            result.fold({ d ->
                Log.e(TAG, d)

                val parsedURL = "https://www.youtube.com/watch?v=5RNkQaDcRAc"
                if (parsedURL != lastURL) {
                    lastURL = parsedURL
                    startYoutubeIntent(parsedURL)
                }
            }, { err ->
                Log.e(TAG, err.toString())
            })
        }
    }
}