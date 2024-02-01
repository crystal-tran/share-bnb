"use strict";

/** Runs on listing/id page render.
 *
 * Calls api to check if listing is booked.
 *
 * If api return is true {booked: true}, hides 'book' and shows 'cancel' button
 * If api returns false {booked: false}, hides 'cancel' and shows 'book' button
 */

$(async function () {
  $("#book").on("click", book);
  $("#cancel").on("click", cancel);

  const urlParams = new URLSearchParams({ listing_id: listingId })
  const response = await fetch(`/api/bookings?${urlParams}`);
  const result = await response.json();

  if ("error" in result) {
    console.log(result.error);
  } else {
    let booked = result.booked;
    if (booked) $("#cancel").show();
    else $("#book").show();
  }
});


/** On click on the 'book' button, it will make an API call to book the listing.
 *
 * API returns booked listing id like:
 * {booked: 1}
 *
 * 'book' button will hide and 'cancel' button will show.
 *
 */

async function book(evt) {
  evt.preventDefault();

  const response = await fetch("/api/book",
    {
      method:"POST",
      body:JSON.stringify({ listing_id: listingId }),
      headers: {
        "content-type": "application/json",
      }
    });

  const result = await response.json();
  console.log("book result:", result)


  if ("error" in result) {
    console.log(result.error);
  } else {
    $("#book").hide();
    $("#cancel").show();
  }
}


/** On click on the 'cancel' button, it will make an API call to cancel
 *  a booked listing.
 *
 * API returns canceled listing id like:
 * {canceled: 1}
 *
 * 'book' button will show and 'cancel' button will hide
 *
 */

async function cancel(evt) {
  evt.preventDefault();

  const response = await fetch("/api/cancel",
  {
    method:"POST",
    body:JSON.stringify({ listing_id: listingId }),
    headers: {
      "content-type": "application/json",
    }
  });
  const result = await response.json();
  console.log("cancel result:", result)

  if ("error" in result) {
    console.log(result.error);
  } else {
    $("#cancel").hide();
    $("#book").show();
  }
}