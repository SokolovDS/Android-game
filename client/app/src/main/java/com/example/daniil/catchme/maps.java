package com.example.daniil.catchme;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Criteria;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v4.content.ContextCompat;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;


public class maps extends FragmentActivity implements OnMapReadyCallback {
    private static final int MY_LOCATION_REQUEST_CODE = 1;

    private GoogleMap mMap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
        Button getCoords = (Button)findViewById(R.id.getCoords);
        getCoords.setOnClickListener(onClickListener);
    }

    String uid;
    double latitude;
    double longitude;
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        Intent getuid = getIntent();
        uid = getuid.getStringExtra("uid");
        latitude=0;
        longitude=0;
        Toast toast = Toast.makeText(getApplicationContext(), uid, Toast.LENGTH_SHORT);
        toast.show();

        // Add a marker in Sydney and move the camera
        LatLng urfu = new LatLng(56.843980, 60.653513);
        mMap.addMarker(new MarkerOptions().position(urfu).title("Marker in URFU"));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(urfu));
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                == PackageManager.PERMISSION_GRANTED) {
            mMap.setMyLocationEnabled(true);
            //Определение местоположения

            LocationManager locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
            Criteria criteria = new Criteria();
            String provider = locationManager.getBestProvider(criteria, true);
            // Getting Current Location
            Location location = locationManager.getLastKnownLocation(provider);
            latitude = location.getLatitude();
            longitude = location.getLongitude();
            if (location != null)
            {
                latitude = location.getLatitude();
                longitude = location.getLongitude();
            }
            //---------------------------------

        } else {
            // Show rationale and request permission.
        }
    }

    //----------------------------
    private final View.OnClickListener onClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            final TextView myTextView = (TextView) findViewById(R.id.cooords);

            //Отправка запроса на получение расстояния
            RequestQueue queue = Volley.newRequestQueue(maps.this);
            String url = "http://artkholl.pythonanywhere.com/get_coord?idd="+uid.substring(1,6)+"&coord="+latitude+"$"+longitude;
            StringRequest stringRequest = new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {
                @Override
                public void onResponse(String response) {
                    // TODO Auto-generated method stub
                    //Toast toast = Toast.makeText(getApplicationContext(), response, Toast.LENGTH_SHORT);
                    //toast.show();
                    myTextView.setText(response);

                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    // TODO Auto-generated method stub
                    //Toast toast = Toast.makeText(getApplicationContext(), "ERROR", Toast.LENGTH_SHORT);
                    //toast.show();

                }
            });

            switch (v.getId()) {
                case R.id.getCoords: {
                    //TextView cooords = (TextView)findViewById(R.id.cooords);
                    //myTextView.setText("sas");
                    queue.add(stringRequest);
                    break;
                }
                default:
                    break;
            }
        }
    };
}
