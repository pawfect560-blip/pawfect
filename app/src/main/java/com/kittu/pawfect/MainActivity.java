package com.kittu.pawfect;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        WebView webView = new WebView(this);
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true); // Needed for Streamlit
        webView.setWebViewClient(new WebViewClient());
        webView.loadUrl("https://pawfect-doc-ai.streamlit.app/");
        setContentView(webView);
    }
}
