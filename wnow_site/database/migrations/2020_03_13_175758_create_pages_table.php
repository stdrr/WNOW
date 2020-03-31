<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreatePagesTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('pages', function (Blueprint $table) {
            $table->bigInteger('pageid');
            $table->string('title', 100);
            $table->string('image', 500);
            $table->string('link', 500);
            $table->mediumText('summary')->nullable();
            $table->string('category', 50);
            $table->timestamp('timestamp');
            $table->primary('pageid');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('pages');
    }
}
