@extends('layouts.app')

@section('page_title')
    {{$article->title}}
@endsection

@section('content')
    <br><br>
    <div class="container-fluid justify-content-center">
        <div class='container-lg justify-content-center py-5'>
            <div class="row justify-content-between">
                <div class="column-lg">
                    <h2><strong>{{$article->title}}</strong></h2>
                </div>
                <div class="column-lg">
                    <a href="https://{{$article->link}}" class="btn btn-primary" target="_blank">Find more on Wikipedia</a>
                </div>
            </div>
            <br><br>
            <img class="img-fluid" src="{{$article->image}}" alt="{{$article->title}} - image">
            <br><br>
            <div class="container-sm-9 justify-content-center">
                <p class="lead text-justify pt-3">{{$article->summary}}</p>
            </div>
        </div>
    </div>
@endsection