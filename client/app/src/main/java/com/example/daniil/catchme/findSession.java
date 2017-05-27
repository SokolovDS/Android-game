package com.example.daniil.catchme;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class findSession extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_find_session);

        Button curSessionBtn = (Button) findViewById(R.id.goToGame);
        curSessionBtn.setOnClickListener(onClickListener);
    }

    private final View.OnClickListener onClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            switch (v.getId()) {
                case R.id.goToGame:
                    Intent toCur = new Intent(findSession.this, curSession.class);
                    startActivity(toCur);
                    break;
                default:
                    break;

            }

        }
    };
}
