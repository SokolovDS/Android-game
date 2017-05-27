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

        //Подключаем нажатие на кнопки
        Button findSessionBtn = (Button) findViewById(R.id.FindSession);
        findSessionBtn.setOnClickListener(onClickListener);
        Button createSessionBtn = (Button) findViewById(R.id.CreateSession);
        createSessionBtn.setOnClickListener(onClickListener);

    }

    //Трекер нажатий
    private final View.OnClickListener onClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            switch (v.getId()) {

                case R.id.FindSession:
                    Intent fSession = new Intent(MainActivity.this, findSession.class);
                    startActivity(fSession);
                    break;
                case R.id.CreateSession:
                    Intent cSession = new Intent(MainActivity.this, createSession.class);
                    startActivity(cSession);
                    break;


                default:
                    break;

            }

        }
    };
}
