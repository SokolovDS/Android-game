package com.example.daniil.catchme;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button mapBtn = (Button) findViewById(R.id.toMap);
        mapBtn.setOnClickListener(onClickListener);

    }

    private final View.OnClickListener onClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            switch (v.getId()) {

                case R.id.toMap:
                    Intent intent = new Intent(MainActivity.this, maps.class);
                    startActivity(intent);
                    break;

                default:
                    break;

            }

        }
    };
}
