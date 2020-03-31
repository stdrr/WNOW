<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

class CreateProcedures extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        DB::unprepared('
            CREATE PROCEDURE sp_page()
            BEGIN
                DECLARE X INT ; DECLARE Y TIMESTAMP ;
                SELECT COUNT(*) INTO X FROM pages ; 
                IF(X > 1000) THEN
                    SELECT MIN(TIMESTAMP) INTO Y FROM pages ;
                    SELECT TIMESTAMPADD(MINUTE, 3, Y) INTO Y ;
                    DELETE FROM pages WHERE TIMESTAMP <= Y ;
                END IF ;
            END
        ');
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        DB::unprepared('DROP PROCEDURE IF EXISTS sp_page');
    }
}
