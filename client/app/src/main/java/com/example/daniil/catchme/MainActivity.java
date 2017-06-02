package com.example.daniil.catchme;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

public class MainActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

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

    //Трекер нажатий
    private final View.OnClickListener onClickListener = new View.OnClickListener() {
        EditText eText;
        TextView tvInfo;
        @Override
        public void onClick(View v) {
            eText = (EditText) findViewById(R.id.editText);
            tvInfo = (TextView) findViewById(R.id.tvInfo);
            //ТЕСТИМ VOLLEY
            RequestQueue queue = Volley.newRequestQueue(MainActivity.this);

            String url = "http://artkholl.pythonanywhere.com/send_email?email="+eText.getText().toString();

            StringRequest stringRequest = new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {

                @Override
                public void onResponse(String response) {
                    // TODO Auto-generated method stub
                    tvInfo.setText("Response => "+response);
                }
            }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    // TODO Auto-generated method stub
                    tvInfo.setText("ERROR 1");

                }
            });
            //---------------------------------------
            switch (v.getId()) {
                case R.id.NickBTN:
                    queue.add(stringRequest);
                    break;
                case R.id.FindSession:
                    Intent fSession = new Intent(MainActivity.this, findSession.class);
                    startActivity(fSession);
                    break;
                /*case R.id.CreateSession:
                    Intent cSession = new Intent(MainActivity.this, createSession.class);
                    startActivity(cSession);
                    break;*/


                default:
                    break;

            }

        }
    };
}
