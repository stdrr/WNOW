<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateTrigger extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        DB::unprepared("
            CREATE TRIGGER profile_create AFTER INSERT ON users
            FOR EACH ROW BEGIN
                INSERT INTO profiles (userid, number_read, economy, entertainment, politics, science_tech, sports) 
                VALUES (new.id, '0', '0', '0', '0', '0', '0');
            END
        ");
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        DB::unprepared('DROP TRIGGER profile_create');
    }
}
