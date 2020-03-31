@extends('layouts.app')

@section('page_title')
    Articles from Wikipedia
@endsection

<?php $base_route = '/news';?>

@section('content')
    <div class="container-fluid">
        <br><br>
        <div class="container-fluid border-bottom py-4 sticky-top bg-white shadow">
            <ul class="nav justify-content-center sticky-top">
                <li class="nav-item">
                  <a class="nav-link text-uppercase" href="{{$base_route}}/For_you"><strong>for you</strong></a>
                </li>
                <li class="nav-item">
                  <a class="nav-link text-uppercase" href="{{$base_route}}/Politics"><strong>politics</strong></a>
                </li>
                <li class="nav-item">
                  <a class="nav-link text-uppercase" href="{{$base_route}}/Economy"><strong>economy</strong></a>
                </li>
                <li class="nav-item">
                    <a class="nav-link text-uppercase" href="{{$base_route}}/Science_tech"><strong>science and tech</strong></a>
                </li>
                <li class="nav-item">
                    <a class="nav-link text-uppercase" href="{{$base_route}}/Sports"><strong>sports</strong></a>
                </li>
                <li class="nav-item">
                    <a class="nav-link text-uppercase" href="{{$base_route}}/Entertainment"><strong>entertainment</strong></a>
                </li>
            </ul>
            
        </div><br><br>
        <div class="container justify-content-center" style="max-width: 90rem">
            <?php $row_counter = 0?>
            @foreach ($pages as $article)
                @if ($row_counter%3==0)
                    <div class="row justify-content-center py-4">
                @endif
                <div class="col-sm-center px-4">
                    <div class="card shadow p-3 mb-5 bg-white rounded" style="width: 27rem;">
                        <div class="container-sm justify-content-center">
                            <h6 class="font-weight-bold text-secondary py-2 text-info">{{$article->category}}</h6>
                        </div>
                        
                        <div class="view view-cascade overlay">
                            <img src="{{$article->image}}" class="card-img-top rounded" alt="Image" style="max-height:18rem; max-width:27rem;">
                        </div>
                        <div class="card-body card-body-cascade text-center">
                            <h4 class="card-title"><strong>{{$article->title}}</strong></h4>
                            
                            <p class="card-text" style="display: block;
                            text-overflow: ellipsis;
                            word-wrap: break-word;
                            overflow: hidden;
                            max-height: 5.4em;
                            line-height: 1.8em;">{{$article->summary}}</p>
                            <a href="{{$base_route}}/page/{{$article->pageid}}" class="btn btn-primary">Read more</a>
                        </div>
                        <div class="card-footer text-muted text-center">
                            {{$article->timestamp}}
                        </div>
                    </div>
                </div>
                @if ($row_counter%3==2)
                    </div><br><br>
                @endif
                <?php $row_counter+=1?>
            @endforeach
        </div>
    </div>
@endsection