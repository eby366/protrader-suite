package com.protrader.suite;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.CookieManager;
import android.webkit.JsResult;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

public class MainActivity extends Activity {

    private WebView webView;

    // URL de votre app hébergée (modifier avec votre URL Netlify)
    private static final String HOSTED_URL = "https://votre-app.netlify.app";
    // Fichier local dans assets/
    private static final String LOCAL_URL  = "file:///android_asset/index.html";
    // true = local (offline), false = URL hébergée
    private static final boolean USE_LOCAL = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                             WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        setContentView(R.layout.activity_main);
        webView = findViewById(R.id.webview);
        configureWebView();
        loadApp();
    }

    private void configureWebView() {
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(true);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        s.setCacheMode(WebSettings.LOAD_DEFAULT);
        s.setMediaPlaybackRequiresUserGesture(false);
        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(webView, true);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) { return false; }
            @Override
            public void onReceivedError(WebView v, int code, String desc, String url) {
                if (!isNetworkAvailable()) v.loadUrl(LOCAL_URL);
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onJsAlert(WebView v, String url, String msg, JsResult r) {
                Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                r.confirm(); return true;
            }
        });
    }

    private void loadApp() {
        if (USE_LOCAL) { webView.loadUrl(LOCAL_URL); return; }
        if (isNetworkAvailable()) { webView.loadUrl(HOSTED_URL); }
        else { webView.loadUrl(LOCAL_URL); Toast.makeText(this,"Mode hors ligne",Toast.LENGTH_LONG).show(); }
    }

    private boolean isNetworkAvailable() {
        ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        if (cm == null) return false;
        NetworkInfo i = cm.getActiveNetworkInfo();
        return i != null && i.isConnected();
    }

    @Override public void onBackPressed() {
        if (webView.canGoBack()) webView.goBack(); else moveTaskToBack(true);
    }
    @Override protected void onPause()   { super.onPause();   webView.onPause(); }
    @Override protected void onResume()  { super.onResume();  webView.onResume(); }
    @Override protected void onDestroy() { if (webView!=null) webView.destroy(); super.onDestroy(); }
}
