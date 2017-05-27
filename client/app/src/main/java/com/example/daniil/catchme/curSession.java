package com.example.daniil.catchme;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class curSession extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cur_session);

        Button toMapBtn = (Button) findViewById(R.id.toMap);
        toMapBtn.setOnClickListener(onClickListener);

    }

    private final View.OnClickListener onClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            switch (v.getId()) {
                case R.id.toMap:
                    Intent toMap = new Intent(curSession.this, maps.class);
                    startActivity(toMap);
                    break;
                default:
                    break;

            }

        }
    };
}
