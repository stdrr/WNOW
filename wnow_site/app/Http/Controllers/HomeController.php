<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Page;
use App\Recommendation;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;

class HomeController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('auth');
    }

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function index()
    {
        $id = Auth::id();
        $pages = DB::table('pages')->join('recommendations', 'pages.pageid', '=', 'recommendations.pageid')
                                ->where('recommendations.userid', $id)->latest('recommendations.id')->get();
        $category = 'For_you';
        if(count($pages) == 0) 
        {
            $pages = DB::table('pages')->where('category', 'Politics')->latest('timestamp')->get();
        }
        return view('index', compact('pages', 'category'));
    }
}
