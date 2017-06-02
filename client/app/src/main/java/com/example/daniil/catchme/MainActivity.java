package com.example.daniil.catchme;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.util.concurrent.TimeUnit;


public class MainActivity extends AppCompatActivity {
    EditText eText;
    TextView tvInfo;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        eText = (EditText) findViewById(R.id.editText);
        tvInfo = (TextView) findViewById(R.id.tvInfo);

        //Подключаем нажатие на кнопки
        //Кнопка никнейм
        Button nicknameBtn = (Button) findViewById(R.id.NickBTN);
        nicknameBtn.setOnClickListener(onClickListener);
        //остальные кнопки
        Button findSessionBtn = (Button) findViewById(R.id.FindSession);
        findSessionBtn.setOnClickListener(onClickListener);
        Button createSessionBtn = (Button) findViewById(R.id.CreateSession);
        createSessionBtn.setOnClickListener(onClickListener);

    }


    class MyTask extends AsyncTask<Void, Void, Void> {

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            tvInfo.setText("Begin");
        }

        @Override
        protected Void doInBackground(Void... params) {
            try {
                TimeUnit.SECONDS.sleep(2);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
            super.onPostExecute(result);
            tvInfo.setText("End");
        }
    }



    //Трекер нажатий
    private final View.OnClickListener onClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            switch (v.getId()) {
                case R.id.NickBTN:
                    String str = eText.getText().toString();
                    Toast msg = Toast.makeText(getBaseContext(),str,Toast.LENGTH_LONG);
                    msg.show();
                    MyTask mt = new MyTask();
                    mt.execute();
                    break;
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
