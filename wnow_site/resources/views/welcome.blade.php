@extends('layouts.app')

@section('page_title')
    What's New On Wiki?
@endsection

@section('content')
    <br><br><br><br><br>
    <div class="container py-10">
        <section class="card wow shadow p-3 mb-5" style="background-image:url('https://wallpaperplay.com/walls/full/1/0/3/91297.jpg')" id="intro">
            <div class="card-body text-white text-center py-5 px-5 my-5">
                <h1 class="mb-4" style="font-size:3rem;">
                <strong>Welcome to What's New On Wiki!</strong>
                </h1>
                <p style="font-size:1.1rem;">
                <strong>The NewsFeed from Wikipedia's pages.</strong>
                </p>
                <br><br>
                <p class="text-center lead text-bold" style="font-size:1.5rem;">
                    Find out the latest modified pages selected for you.<br>
                    Sign in or register, dive into Wikipedia's content<br> and let us learning from your tastes.<br>
                    Get started!<br><br><br>
                </p>
                <div class="row justify-content-center">
                    <div class="col-sm">
                        <a href="{{ route('login') }}" class="btn bg-success rounded text-white px-5 border border-white" style="font-size:1.8rem;">Sign in</a>
                        <a href="{{ route('register') }}" class="btn rounded text-white px-5 border border-white" style="font-size:1.8rem;">Register</a>
                    </div>
                </div>

            </div>
        </section>
    </div>
@endsection

 