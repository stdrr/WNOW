<?php

namespace App\Http\Controllers;

use App\Page;
use App\Recommendation;
use App\Profile;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;

class PagesController extends Controller
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
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index($category)
    {
        $pages = NULL;
        if($category=='Science_tech') 
        {
            $pages = DB::table('pages')->where('category', 'Science and Technology')->latest('timestamp')->get();
        }
        else {
            $pages = DB::table('pages')->where('category', $category)->latest('timestamp')->get();
        }
        return view('index', compact('pages', 'category'));
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Pages  $pages
     * @return \Illuminate\Http\Response
     */
    public function show($pageid)
    {
        $update_profile = function($u_f, $p_f, $n) {return ((($u_f * $n) + $p_f) / ($n + 1));};
        $page_profile = ['Economy'=>0, 'Entertainment'=>0, 'Politics'=>0, 'Science and Technology'=>0, 'Sports'=>0];
        $article = Page::findOrFail($pageid);
        $user_profile = Profile::findOrFail(Auth::id());
        $page_profile[$article->category] += 1;
        $user_profile->economy = $update_profile($user_profile->economy, $page_profile['Economy'], $user_profile->number_read);
        $user_profile->entertainment = $update_profile($user_profile->entertainment, $page_profile['Entertainment'], $user_profile->number_read);
        $user_profile->politics = $update_profile($user_profile->politics, $page_profile['Politics'], $user_profile->number_read);
        $user_profile->science_tech = $update_profile($user_profile->science_tech, $page_profile['Science and Technology'], $user_profile->number_read);
        $user_profile->sports = $update_profile($user_profile->sports, $page_profile['Sports'], $user_profile->number_read);
        $user_profile->number_read += 1;
        $user_profile->save();
        return view('show', compact('article'));
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Pages  $pages
     * @return \Illuminate\Http\Response
     */
    public function edit(Pages $pages)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Pages  $pages
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Pages $pages)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Pages  $pages
     * @return \Illuminate\Http\Response
     */
    public function destroy(Pages $pages)
    {
        //
    }
}
