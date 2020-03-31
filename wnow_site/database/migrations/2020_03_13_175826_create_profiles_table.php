<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateProfilesTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('profiles', function (Blueprint $table) {
            $table->foreignId('userid');
            $table->integer('number_read')->default(0);
            $table->double('economy', 10, 9);
            $table->double('entertainment', 10, 9);
            $table->double('politics', 10, 9);
            $table->double('science_tech', 10, 9);
            $table->double('sports', 10, 9);
            $table->primary('userid');
            $table->foreign('userid')
                    ->references('id')->on('users')
                    ->onDelete('cascade')
                    ->onUpdate('cascade');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('profiles');
    }
}
