---
layout: post
title: "Highway Math"
excerpt: "Build some intuition for how speed affects travel time and safety."
tags: misc
date: 2024-03-10
modified_date: 2024-03-10
katex: True
---

{{ page.excerpt }}

<style>
p input {
  border-radius: 5px;
  border-width: 1px;
  display: inline;
  font-family: inherit;
  font-size: inherit;
  color: inherit;
  padding: none;
  width: 1.5em;
  background: none;
}

/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}
</style>

<p style="text-align: center;">
Your original trip of
<input id="distance" type="number" min=1 max=2000 step=1 value=60 onmousewheel="onWheel()"/>
miles, at
<input id="oldSpeed" type="number" min=1 max=150 step=1 value=60 onmousewheel="onWheel()"/>
mph would take
<span id='time'>50</span>
minutes.
</p>
<p style="text-align: center;">
Going
<input id="newSpeed" type="number" min=1 max=150 step=1 value=65 onmousewheel="onWheel()"/>
mph
<span id='saveadd'>saves</span>
<span id='timeChange'>5</span>
minutes,
<span id='butand'>but increases</span>
your risk of an accident with injury by
</p>
<h3 style="text-align: center;">
<span id='ARR'>38%.</span>
</h3>
<h3 style="text-align: center;">
<strong><em>Slow Down.</em></strong>
</h3>

<p style="text-align: center;">
At your <em>original</em> speed, if your reaction time is
<input id="reactionTimeS" type="number" min="0.1" max="2" step="0.1" value="0.5" onmousewheel="onWheel()"/>
seconds,
your approximate stopping distance is
</p>
<h3 style="text-align: center;">
<span id="stoppingDistance">200 feet.</span>
</h3>
<p style="text-align: center;">
The typical car length is <em>15 feet.</em>
</p>

<h3 style="text-align: center;">
<strong><em>Keep More Distance.</em></strong>
</h3>

Even if you think you can stop in much less than that distance,
do you trust the person behind you to? Do you trust their reaction time?


## Discussion and References

### Accident Risk
The computation of increased accident risk is based on an updated 2019
analysis below.
They have a number of different models
they evaluate, but loosely there seems to be a strong
power function relationship among relative risk and relative speed.
Playing with the exponent doesn't change the result meaningfully.

Updated estimates of the relationship between speed and road safety at the aggregate and individual levels.
<br/>
_Elvik, Rune, Anna Vadeby, Tove Hels, and Ingrid Van Schagen._
<br/>
Accident Analysis & Prevention 123 (2019): 114-122.
(pdf available on first Scholar search)


### Stopping Distance
Stopping distance is similar, where the computation can vary
heavily based on the particular situation being studied.
The factors involve may seem extremely conservative,
but even if you cut reaction time to 0,
from 60MPH braking distances are around 170 feet.
[NACTO: Vehicle Stopping Distance and Time](https://nacto.org/references/a-hrefdocsusdgvehicle_stopping_distance_and_time_upenn/)

The formula used here is from this calculator:
[Stopping Distance Calculator](https://www.omnicalculator.com/physics/stopping-distance),
which cites the [AASHTO](https://transportation.org) but I could
not find a direct source from AASHTO.
(also check out [Car Crash Calculator](https://www.omnicalculator.com/physics/car-crash-force))

### Reaction Time
If you want to test what your "sterile" reaction time would be:
[Reaction Time Test](https://humanbenchmark.com/tests/reactiontime).

The distribution shown there is likely a gross underestimate of
what your typical response time would be on the road, for a number of factors
including anticipating the stimulus, the stimulus intensity (portion of view, green to red),
and selection bias (the people normally using that site are frequent video game players/professionals).
Other recent studies on typical reaction times are closer to 500ms on average,
and you can find transportation sources indicating greater than 1 second
for practical estimates!

The Effects of driver age and gender on vehicle stopping distance under different speeds. 
<br/>
_Hichim, Majid Farag, Ahmed Shany Khusheef, and S. H. Raheemah._
<br/>
Eur Transp 2020.80 (2020): 1-11.
(pdf available on first Scholar search)

Also, apparently the study of 
human reaction times is called
[Mental Chronometry](https://en.wikipedia.org/wiki/Mental_chronometry),
fun.


### Metric?
The relative risk computation cancels the constant factor so it doesn't matter
except for helping with intuition.



<script>
    function onWheel() {}
</script>

<script>

    // input variables
    const dist = document.getElementById("distance");
    const oldspd = document.getElementById("oldSpeed");
    const newspd = document.getElementById("newSpeed");
    const react = document.getElementById("reactionTimeS");

    var d = dist.value;
    var os = oldspd.value;
    var ns = newspd.value;
    var rt = react.value;

    // things to watch
    dist.addEventListener("input", updateDist);
    oldspd.addEventListener("input", updateOS);
    newspd.addEventListener("input", updateNS);
    react.addEventListener("input", updateRT);

    const oldtime = document.getElementById("time");
    const timesave = document.getElementById("timeChange");
    const arr = document.getElementById("ARR");

    const sa = document.getElementById("saveadd");
    const ba = document.getElementById("butand");

    const sd = document.getElementById("stoppingDistance");

    function updateDist(e) {
        d = e.target.valueAsNumber;
        updateFuncs();
    }
    function updateOS(e) {
        os = e.target.valueAsNumber;
        updateFuncs();
    }
    function updateNS(e) {
        ns = e.target.valueAsNumber;
        updateFuncs();
    }
    function updateRT(e) {
        rt = e.target.valueAsNumber;
        updateFuncs();
    }

    function updateFuncs() {
        console.log('Updating computed values after input val change');
        
        // basic d = r*t
        oldtime.textContent = (d*60 / os).toFixed(2);

        // difference in time after new speed
        var timediff = (((ns - os)/ns)*(d*60/os)).toFixed(2);
        if (Math.sign(timediff) == -1) {
            sa.textContent = "adds";
            ba.textContent = "and decreases";
            ba.style.color = "Green";
            arr.style.color = "Green";
        } else {
            sa.textContent = "saves";
            ba.textContent = "but increases";
            ba.style.color = "Red";
            arr.style.color = "Red";
        }
        timesave.textContent = Math.abs(timediff);

        // from 2019 meta study of accident rates based on speed
        var arrval = (100 - 100*(ns / os)**3.763).toFixed(2);

        arr.textContent = Math.abs(arrval) + "%.";

        // from https://www.omnicalculator.com/physics/stopping-distance
        // conversion from miles to kilometers (1.6) back to feet (3)
        sd.textContent = (3*((0.278 * rt * os*1.6) + (os*1.6)**2 / (254 * (0.7 + 0)))).toFixed(0) + " feet.";
        sd.style.color = "Red";

    }

    updateFuncs();

</script>





<!---
We all know that speed is distance over time:

$$ r = \frac{d}{t} $$

But it's harder to understand the "inverse" problem that we typically
care about most in the real world:

$$ t = \frac{d}{r} $$

How long will it take to get somewhere? Generally we have the distance
fixed, like the commute from home to work. When deciding on speeds,
especially when driving, our bad-calculator-brains generally
see a very strong relationship with increasing our speed $r$ to decreasing
our time $t$. Of course this relationship exists, but it's harder
to understand the _relative_ time gains when going different speeds.

## Quick Algebra

We can figure this out using the fact that the distance we'll be going, regardless
of speed or time, is fixed.

$$ d = r_1 t_1, \quad d = r_2 t_2 $$

We can set them equal and look only at the speed and time relationship:

$$ r_1 t_1 = r_2 t_2 $$

Let's say we want to know how much time we'll save, $ t_1 - t_2 $, if we increase
our speed from $r_1$ to $r_2$. With some algebra manipulation:

$$ t_1 - t_2 = t_1 - \frac{r_1}{r_2}t_1 $$

$$ t_1 - t_2 = \frac{r_2 -r_1}{r_2} t_1 $$

OK, so the time we gain is porportional to the increase in our speed divided by our new speed.
This is really hard to get an intuition for, so lets plug in some numbers.

Say you're going 55mph and your journey generally takes 1 hour to complete. Let's see how much time
you'll save by going 60mph:

$$ \frac{60 - 55}{60}*(1\text{ hour}) = \frac{5}{60}(60\text{ minutes}) = 5\text{ minutes} $$

So if you were originally going to get to your destination at 5pm, you'll now get there at 5:05pm.
The important part here is that this is relative to your new speed. If you're going from 75 to 80
for a trip that previously took an hour, you'll now only save 3 minutes and 45 seconds! 


### Safety
Recent meta analyses on how speed affects accidents rates suggests that a power law roughly applies
for computing the accident reduction rate (ARR):

$$ ARR = 1 - \left(\frac{slower\ speed}{faster\ speed}\right)^{3.763} $$



60 mph is 88 feet per second. The average car length is around 15 feet. The average reaction time
of [people who often test](https://humanbenchmark.com/tests/reactiontime) is more than 250 milliseconds.
In that time, at 60 mph, you would have gone 22 feet.


American Association of State Highway and Transportation Officials

This is a test of a basic inline numbered input,
<input id="distancetest" type="number" min=1 max=1000 step=1 value=60 onmousewheel="onWheel()"/>
, where it shoulbe be before this part.

<p id='speedtest'>50</p>

-->
