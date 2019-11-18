// procédures pour Moodle
moodle_href = "/"

//function GoToMoodleHomePage()
//    {
//    var LastMoodleHref = "<?php echo json_encode($_SERVER['HTTP_REFERER']); ?>";
//    window.location.href LastMoodleHref;
//    }

function GoToMoodleHomePage()
{
    // window.location.href="/moodle"
    // window.location.href="/course/index.php?categoryid=11"
//    alert("GoToMoodleHomePage = " + moodle_href);
    window.location.href = moodle_href;
}
