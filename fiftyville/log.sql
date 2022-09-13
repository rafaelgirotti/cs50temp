-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports
   ...> WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';
-- get description of crime scene

SELECT transcript FROM interviews
   ...> WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';
-- get transcript of interviews related to the bakery

SELECT name FROM people
   ...> JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
   ...> WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25
   ...> AND activity = 'exit';
-- get bakery security logs + license plates and join with people's license plate from people's table
-- at time and minute reported on 1st interview
-- names: Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey

SELECT name FROM people
   ...> JOIN bank_accounts ON bank_accounts.person_id = people.id
   ...> JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
   ...> WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';
-- get atm transaction from Leggett Street from 2nd report, and join with bank accounts and people id
-- matching names from 1st report: Bruce, Diana, Iman, Luca

SELECT name FROM people
   ...> JOIN passengers ON passengers.passport_number = people.passport_number
   ...> WHERE passengers.flight_id = (
   ...> SELECT id FROM flights
   ...> WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (
   ...> SELECT id FROM airports WHERE city = 'Fiftyville')
   ...> ORDER BY hour,minute
   ...> LIMIT 1);
-- get passengers for the earliest flight from fiftyville on the next day
-- matching names from 2nd report: Bruce, Luca

SELECT name FROM people
   ...> JOIN phone_calls ON phone_calls.caller = people.phone_number
   ...> WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;
-- get phone calls from time at 3
-- matching names from 3rd report: Bruce
-- thief is Bruce

SELECT city FROM airports
   ...> WHERE id = (SELECT destination_airport_id FROM flights
   ...> WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (
   ...> SELECT id FROM airports WHERE city = 'Fiftyville')
   ...> ORDER BY hour,minute
   ...> LIMIT 1);
-- get city Bruce's escaped to, result is New York City

SELECT phone_number FROM people WHERE name = 'Bruce';
-- get Bruce's phone number for next part: (367) 555-5533

SELECT name FROM people WHERE phone_number = (
   ...> SELECT receiver FROM phone_calls
   ...> WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60 AND caller ='(367) 555-5533');
-- get receiver from caller (367) 555-5533. The receiver's name is Robin. Very funny CS50.